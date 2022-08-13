import socket
from datetime import datetime
import time
import numpy as np
# from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import io
from TLDFMX_wrapper import DM
import TLDFMX_wrapper

localIP = "localhost"
localPort = 10022
bufferSize = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

num_z = 12
z_modes_to_optimize = range(num_z)  # [10, 11, ]  # range(num_z)
numsteps = 5
min_amplitude = -0.1
max_amplitude = 0.1
num_frames = 5
metric_map = np.zeros((num_z, numsteps))

print('Waiting for trigger for baseline')
for i in range(10):
    if i == 0:
        print('Taking baseline frames', end='')
    else:
        print('.', end='')
    float(UDPServerSocket.recvfrom(bufferSize)[0])
print('')

print("Starting opt loop")
steps = np.linspace(min_amplitude, max_amplitude, numsteps)
t0 = time.time()
with TLDFMX_wrapper.DM_Context(0) as dm:
    for z_mode in z_modes_to_optimize:
        for stepnum, step in enumerate(steps):
            mirror_pattern = dm.calculate_single_zernicke_pattern(z_mode, step)
            dm.set_segment_voltages(mirror_pattern)
            dm.set_segment_voltage_setpoints(mirror_pattern)
            metrics = []
            for n in range(num_frames):
                # print("waiting for packet")
                metric = float(UDPServerSocket.recvfrom(bufferSize)[0])
                print(f"Mode: {z_mode}  Step: {step} Metric: {metric}")
                if n >= 1:
                    metrics.append(metric)
            metric_map[z_mode, stepnum] = np.asarray([metrics]).mean()
        mirror_pattern = dm.calculate_single_zernicke_pattern(z_mode, steps[metric_map[z_mode, :].argmax()])
        dm.set_segment_voltages(mirror_pattern)
        dm.set_segment_voltage_setpoints(mirror_pattern)
print(f'Opt loop done in {time.time() - t0} seconds')

now = datetime.now()
np.save(f'metric_map_{now.strftime("%Y_%m_%d_%H_%M")}', metric_map)
best_mode_settings = steps[metric_map.argmax(axis=1)]
np.save(f'best_mode_settings_{now.strftime("%Y_%m_%d_%H_%M")}', best_mode_settings)

plt.figure()
plt.imshow(metric_map, aspect='auto')
plt.colorbar()
plt.xlabel('Step')
plt.ylabel('Zmode')
plt.savefig(f'metric_map_{now.strftime("%Y_%m_%d_%H_%M")}')
plt.show()
