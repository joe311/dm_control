from ctypes import *
from functools import wraps
from collections import namedtuple
import numpy as np

dfm = WinDLL(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll')
dfmx = WinDLL(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll')


def handle_error(DFMfunc):
    """Wraps function to translate error codes into readable text"""

    @wraps(DFMfunc)
    def handle(*args, **kwargs):
        ret = DFMfunc(*args, **kwargs)
        if ret < 0:
            pBuf = create_string_buffer(512)
            dfm.TLDFM_error_message(VI_NULL, ret, pBuf)
            print("Error:", pBuf.value)
            # raise IOError
        return ret

    return handle


VI_NULL = 0
VI_TRUE = 1
VI_FALSE = 0

device_info = namedtuple("device_info", "instrumentName serialNumber deviceAvailable resourceName", )
params = namedtuple("params",
                    "minimumZernikeAmplitude maximumZernikeAmplitude maximumZernikeCount measurementSteps relaxSteps")


class DM:
    def __init__(self, device_num):
        device_info = self.device_info(device_num)
        resourceName = device_info.resourceName
        # initiate the instrument driver session
        self.instrumentHandle = c_long(0)  # ViSession is long
        # print(instrumentHandle)
        print(f"Connecting to {resourceName}")
        handle_error(dfmx.TLDFMX_init)(resourceName, VI_TRUE, VI_TRUE, byref(self.instrumentHandle))
        # file:///C:/Program%20Files%20(x86)/IVI%20Foundation/VISA/WinNT/TLDFMX/Manual/TLDFMX_files/FunctTLDFMX_init.html
        print("InstrumentHandle: ", self.instrumentHandle)

    # @classmethod
    # def from_device_num(cls, device_num=0):
    #     device_info = cls.device_info(device_num)
    #     return cls.__init__(device_info.resourceName)

    @staticmethod
    def device_info(device_num=0):
        # Get DM info and print them
        manufacturer = create_string_buffer(256)
        instrumentName = create_string_buffer(28)
        serialNumber = create_string_buffer(28)
        deviceAvailable = c_bool()
        resourceName = create_string_buffer(256)
        dfm.TLDFM_get_device_information(VI_NULL, device_num, byref(manufacturer), byref(instrumentName),
                                         byref(serialNumber),
                                         byref(deviceAvailable), byref(resourceName))
        return device_info(instrumentName.value, serialNumber.value, deviceAvailable.value, resourceName.value)
        # print(instrumentName.value)
        # print(serialNumber.value)
        # print(deviceAvailable.value)
        # print(resourceName.value)

    @property
    def device_count(self):
        dev_num = c_uint(0)
        ret = handle_error(dfm.TLDFM_get_device_count)(VI_NULL, byref(dev_num))  # Get the number of devices available
        return dev_num.value

    def close(self):
        return handle_error(dfmx.TLDFMX_close(self.instrumentHandle))

    @property
    def hysteresis_comp_enalded(self):
        hysteresis_comp_enalded = c_bool()
        #	2nd parameter determines the target item.
        # 0   T_MIRROR
        # 1   T_TILT
        dfm.TLDFM_enabled_hysteresis_compensation(self.instrumentHandle, 0, hysteresis_comp_enalded)
        return hysteresis_comp_enalded

    def get_params(self):
        minimumZernikeAmplitude = c_double(1)
        maximumZernikeAmplitude = c_double(1)
        maximumZernikeCount = c_int(1)
        measurementSteps = c_int(1)
        relaxSteps = c_int(1)
        handle_error(dfmx.TLDFMX_get_parameters)(self.instrumentHandle, byref(minimumZernikeAmplitude),
                                                 byref(maximumZernikeAmplitude), byref(maximumZernikeCount),
                                                 byref(measurementSteps), byref(relaxSteps))
        return params(minimumZernikeAmplitude.value, maximumZernikeAmplitude.value, maximumZernikeCount.value,
                      measurementSteps.value, relaxSteps.value)
        # print("params:", minimumZernikeAmplitude.value, maximumZernikeAmplitude.value, maximumZernikeCount.value,
        #       measurementSteps.value, relaxSteps.value)

    @property
    def segment_count(self):
        segmentCount = c_int(0)
        dfm.TLDFM_get_segment_count(self.instrumentHandle, byref(segmentCount))
        return segmentCount.value

    def calculate_single_zernicke_pattern(self, zernicke_mode, zernicke_amp):
        mirrorPattern = (c_double * 40)(0)
        bitflag = self.zernicke_mode_bitflags(zernicke_mode)
        ret = handle_error(dfmx.TLDFMX_calculate_single_zernike_pattern)(self.instrumentHandle, bitflag,
                                                                         c_double(zernicke_amp),
                                                                         byref(mirrorPattern))
        return mirrorPattern

    @staticmethod
    def zernicke_mode_name(zernicke_mode):
        mode_names = ['Ast45',
                      'Defocus',
                      'Ast0',
                      'Trefoil Y',
                      'Coma X',
                      'Coma Y',
                      'Trefoil X',
                      'TetY',
                      'SAstY',
                      'Spherical',
                      'SAstX',
                      'TetX', ]
        return mode_names[zernicke_mode]

    @staticmethod
    def zernicke_mode_bitflags(zernicke_mode):
        bitflags = [0x00000001,  # Z4
                    0x00000002,  # Z5
                    0x00000004,  # Z6
                    0x00000008,  # Z7
                    0x00000010,  # Z8
                    0x00000020,  # Z9
                    0x00000040,  # Z10
                    0x00000080,  # Z11
                    0x00000100,  # Z12
                    0x00000200,  # Z13
                    0x00000400,  # Z14
                    0x00000800]  # Z15
        return bitflags[zernicke_mode]

    def calculate_zernicke_pattern(self, zernick_mode_amplitudes):
        # mirror voltage pattern Zernike
        zernikes = 0xFFFFFFFF  # All zernicke mode (z4-z15) bitflag
        # z_amps =  # -1 to 1 range??

        empty_amps = c_double * 12  # ViReal64 array
        z_amps = empty_amps(*zernick_mode_amplitudes)

        mirrorPattern = (c_double * 40)(0)
        ret = handle_error(dfmx.TLDFMX_calculate_zernike_pattern)(self.instrumentHandle, zernikes, z_amps,
                                                                  byref(mirrorPattern))
        return mirrorPattern

    def set_segment_voltages(self, mirrorPattern):
        ret = handle_error(dfm.TLDFM_set_segment_voltages)(self.instrumentHandle, mirrorPattern)
        return ret

    def set_segment_voltage_setpoints(self, mirrorPattern):
        ret = handle_error(dfmx.TLDFMX_set_voltages_setpoint)(self.instrumentHandle, mirrorPattern)
        return ret

    @property
    def segment_voltages(self):
        raise NotImplementedError

    @property
    def tilt_count(self):
        tiltCount = c_int(0)
        handle_error(dfm.TLDFM_get_tilt_count)(self.instrumentHandle, byref(tiltCount))
        return tiltCount.value

    def set_tilt(self, amplitude, angle):
        # TiltAngle = 0  # Range: -180 - +180 (180:left -90:down, 0:right, +90:up)
        handle_error(dfm.TLDFM_set_tilt_amplitude_angle)(self.instrumentHandle, amplitude, angle)


class DM_Context:
    def __init__(self, device_num=0):
        self.device_num = device_num

    def __enter__(self):
        self._dm = DM(device_num=self.device_num)
        return self._dm

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._dm.close()


if __name__ == "__main__":
    # from matplotlib import pyplot as plt
    import time

    duration = 1
    updates_per_sec = 10
    timebase = np.linspace(0, duration, duration * updates_per_sec)
    waveform = (timebase % 1) - 0.5

    # plt.figure()
    # plt.plot(timebase, waveform)
    # plt.show()

    print('starting waveform loop')
    with DM_Context(0) as dm:
        z4 = 0  # Ast45
        z5 = .2  # Defocus
        z6 = 0  # Ast0
        z7 = 0  # Trefoil Y
        z8 = 0  # Coma X
        z9 = 0  # Coma Y
        z10 = .2  # Trefoil X
        z11 = 0  # TetY
        z12 = 0  # SAstY
        z13 = 0  # Spherical
        z14 = 0  # SAstX
        z15 = 0  # TetX

        mirror_pattern = dm.calculate_zernicke_pattern([z4, z5, z6, z7, z8, z9, z10, z11, z12, z13, z14, z15])
        print([i for i in mirror_pattern])
        dm.set_segment_voltage_setpoints(mirror_pattern)
        dm.set_segment_voltages(mirror_pattern)

        z6 = 1
        mirror_pattern = dm.calculate_zernicke_pattern([z4, z5, z6, z7, z8, z9, z10, z11, z12, z13, z14, z15])
        print('test')
        print([i for i in mirror_pattern])
        print('test2')
        mirror_pattern = dm.calculate_zernicke_pattern([0, ] * 12)
        dm.set_segment_voltage_setpoints(mirror_pattern)
        dm.set_segment_voltages(mirror_pattern)

        # print(dm)
        # # dm = DM(0)
        # for wavepoint in waveform:
        #     # print(wavepoint)
        #     mirror_pattern = dm.calculate_single_zernicke_pattern(7, wavepoint)
        #     dm.set_segment_voltages(mirror_pattern)
        #     time.sleep(1 / updates_per_sec)
        #     print('.', end='')
    print("finished")
