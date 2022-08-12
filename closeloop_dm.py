import numpy as np
from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
from skimage import io
import matplotlib.gridspec as gridspec
import pandas as pd


num_z = 12
numsteps = 8
min_amplitude = -0.5
max__amplitude = 0.5
num_frames = 6
metric_map = np.zeros(num_z, steps)


def metric(frame):
  np.abs(fftshift(fft2(frame)))
  return metricness
rec_frame()


for z_modes in range(num_z):
  steps = np.linspace(min, max, numsteps)
  for stepnum, step in enumerate(steps):
    DM(z_modes, step)
    frames = []
    for n in range(num_frames):
      frame = rec_frame()
      frames.append(frame) 
    frame_metric = np.asarray([metric(frame) for frame in frames])
    metric_map[z_mode, stepnum] = frame_metric.mean()
  DM(z_mode, steps[metric_map[z_mode, :].argmax()])
