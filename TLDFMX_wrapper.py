from ctypes import *
from functools import wraps

dfm = WinDLL(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll')
dfmx = WinDLL(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll')


def handle_error(DFMfunc):
    """Wraps function to translate error codes into readable text"""

    @wraps(DFMfunc)
    def handle(*args, **kwargs):
        print()
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
# class DM:
#     def __init__(self, serial='serial'):
#         self.instrumentHandle = c_long(0)  # ViSession is long
#         self.serial = serial
#
#     def __enter__(self):
#         handle_error(dfmx.TLDFMX_init)(self.serial, False, False, self.instrumentHandle)
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         handle_error(dfmx.TLDFMX_close(self.instrumentHandle))
#
#     @property
#     def hysteresis_comp_enalded(self):
#         hysteresis_comp_enalded = c_bool()
#         #	2nd parameter determines the target item.
#         # 0   T_MIRROR
#         # 1   T_TILT
#         dfm.TLDFM_enabled_hysteresis_compensation(self.instrumentHandle, 0, hysteresis_comp_enalded)
#         return hysteresis_comp_enalded

dev_num = c_uint(0)
ret = dfm.TLDFM_get_device_count(VI_NULL, byref(dev_num))  # Get the number of devices available
print(dev_num.value)

# Get DM info and print them
manufacturer = create_string_buffer(256)
instrumentName = create_string_buffer(28)
serialNumber = create_string_buffer(28)
deviceAvailable = c_bool()
resourceName = create_string_buffer(256)
dfm.TLDFM_get_device_information(VI_NULL, 0, byref(manufacturer), byref(instrumentName), byref(serialNumber),
                                 byref(deviceAvailable), byref(resourceName))
# print(f"First device: {}")
print(instrumentName.value)
print(serialNumber.value)
print(deviceAvailable.value)
print(resourceName.value)

# initiate the instrument driver session
instrumentHandle = c_long(0)  # ViSession is long
print(instrumentHandle)
handle_error(dfmx.TLDFMX_init)(resourceName.value, VI_TRUE, VI_TRUE, byref(instrumentHandle))
# file:///C:/Program%20Files%20(x86)/IVI%20Foundation/VISA/WinNT/TLDFMX/Manual/TLDFMX_files/FunctTLDFMX_init.html
print(instrumentHandle)
# print(hystersis_comp_enalded)

minimumZernikeAmplitude = c_double(1)
maximumZernikeAmplitude = c_double(1)
maximumZernikeCount = c_int(1)
measurementSteps = c_int(1)
relaxSteps = c_int(1)
handle_error(dfmx.TLDFMX_get_parameters)(instrumentHandle, byref(minimumZernikeAmplitude),
                                         byref(maximumZernikeAmplitude), byref(maximumZernikeCount),
                                         byref(measurementSteps), byref(relaxSteps))
print("params:", minimumZernikeAmplitude.value, maximumZernikeAmplitude.value, maximumZernikeCount.value,
      measurementSteps.value, relaxSteps.value)

# TLDFMX_get_parameters
segmentCount = c_int(0)
dfm.TLDFM_get_segment_count(instrumentHandle, byref(segmentCount))
print(segmentCount.value)

# mirror voltage pattern Zernike
zernikes = 0xFFFFFFFF  # All zernicke mode (z4-z15) bitflag
# z_amps =  # -1 to 1 range??
z4 = 0  # Ast45
z5 = 0  # Defocus
z6 = 0  # Ast0
z7 = 0  # Trefoil Y
z8 = 0  # Coma X
z9 = 0  # Coma Y
z10 = 0  # Trefoil X
z11 = 0  # TetY
z12 = 0  # SAstY
z13 = 0  # Spherical
z14 = 0  # SAstX
z15 = 0  # TetX
empty_amps = c_double * 12  # ViReal64 array
z_amps = empty_amps(*[z4, z5, z6, z7, z8, z9, z10, z11, z12, z13, z14, z15])
# z_amps = empty_amps(1)

mirrorPattern = (c_double * 40)(0)
# print(mirrorPattern)
# ret = handle_error(dfmx.TLDFMX_calculate_single_zernike_pattern)(instrumentHandle, c_uint(1), c_double(0.5), byref(
#     mirrorPattern))  # mirror voltage pattern according to a single desired 'Zernike Amplitude'
ret = handle_error(dfmx.TLDFMX_calculate_zernike_pattern)(instrumentHandle, zernikes, z_amps,
                                                          byref(mirrorPattern))  # multiple desired 'Zernike Amplitude'

print(*mirrorPattern)
print('Setting voltages')
ret = handle_error(dfm.TLDFM_set_segment_voltages)(instrumentHandle, mirrorPattern)

# Tilt
print('Playing with tilt')
TiltAmplitude = 0   # Range: 0.0 - 1.0
TiltAngle = 0   # Range: -180 - +180 (180:left -90:down, 0:right, +90:up)

# TLDFMX_get_parameters Tilt
tiltCount = c_int(0)
dfm.TLDFM_get_tilt_count(instrumentHandle, byref(tiltCount))
print("TiltCount:", tiltCount.value)
dfm.TLDFM_set_tilt_amplitude_angle(instrumentHandle, TiltAmplitude, TiltAngle) # apply desired 'tilt amplitude & angle'

# Terminates the software connection
dfmx.TLDFMX_close(instrumentHandle)
