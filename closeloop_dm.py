import numpy as np
from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
from skimage import io
import matplotlib.gridspec as gridspec
from TLDFMX_wrapper import DM
# import pandas as pd

import socket

localIP = "localhost"
localPort = 10022
bufferSize = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")


num_z = 12
z_modes_to_optimize = range(num_z)
numsteps = 8
min_amplitude = -0.3
max_amplitude = 0.3
num_frames = 6
metric_map = np.zeros((num_z, numsteps))

# dm = DM(0)
for z_mode in z_modes_to_optimize:
    steps = np.linspace(min_amplitude, max_amplitude, numsteps)
    for stepnum, step in enumerate(steps):
        # dm.set_segment_voltages(dm.calculate_single_zernicke_pattern(z_mode, step))
        metrics = []
        for n in range(num_frames):
            metric = float(UDPServerSocket.recvfrom(bufferSize)[0])
            print(f"Mode: {z_mode}  Step: {step} Metric: {metric}")
            if n >= 1:
                metrics.append(metric)
        metric_map[z_mode, stepnum] = np.asarray([metrics]).mean()
    # dm.set_segment_voltages(dm.calculate_single_zernicke_pattern(z_mode, steps[metric_map[z_mode, :].argmax()]))
# dm.close()
