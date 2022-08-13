import socket
from datetime import datetime
import time
import numpy as np
# from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
import TLDFMX_wrapper


metric_map = np.load('metric_map_2022_08_12_22_58.npy')
num_z = 12
z_modes_to_optimize = range(num_z) #[10, 11, ]  # range(num_z)
numsteps = 7
min_amplitude = -0.3
max_amplitude = 0.3
num_frames = 6
steps = np.linspace(min_amplitude, max_amplitude, numsteps)
best_mode_settings = steps[metric_map.argmax(axis=1)]

with TLDFMX_wrapper.DM_Context(0) as dm:
    mirror_pattern = dm.calculate_zernicke_pattern(best_mode_settings)
    dm.set_segment_voltages(mirror_pattern)
    dm.set_segment_voltage_setpoints(mirror_pattern)

