import socket
from datetime import datetime
import time
import numpy as np
# from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt


metric_map = np.load('metric_map_2022_08_12_22_58.npy')
plt.figure()
plt.imshow(metric_map, aspect='auto')
plt.colorbar()
plt.xlabel('Step')
plt.ylabel('Zmode')
# plt.savefig(f'metric_map_{now.strftime("%Y_%m_%d_%H_%M")}')
plt.show()
