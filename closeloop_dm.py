import numpy as np
from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
from skimage import io
import matplotlib.gridspec as gridspec
from TLDFMX_wrapper import DM
# import pandas as pd

num_z = 12
numsteps = 8
min_amplitude = -0.5
max__amplitude = 0.5
num_frames = 6
metric_map = np.zeros(num_z, numsteps)

#TODO server receiving loop
dm = DM(0)
for z_mode in range(num_z):
    steps = np.linspace(min, max, numsteps)
    for stepnum, step in enumerate(steps):
        dm.set_segment_voltages(dm.calculate_single_zernicke_pattern(z_mode, step))
        metrics = []
        for n in range(num_frames):
            metric = float(UDPServerSocket.recvfrom(bufferSize)[0])
            metrics.append(metric)

        metric_map[z_mode, stepnum] = np.asarray([metrics]).mean()
    dm.set_segment_voltages(dm.calculate_single_zernicke_pattern(z_mode, steps[metric_map[z_mode, :].argmax()]))
dm.close()