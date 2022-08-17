import socket
from datetime import datetime
import time
import numpy as np
# from numpy.fft import fft2, fftshift
from matplotlib import pyplot as plt
from galsim import zernike
# from zernike.zernike import RZern

metric_map = np.load('/Users/benoitc/Documents/Courses/CSHL/Project/SLM/dm_control-master/metric_map_2022_08_12_23_16.npy')

plt.figure()
plt.imshow(metric_map, aspect='auto')
plt.colorbar()
plt.xlabel('Step')
plt.ylabel('Zmode')
# plt.savefig(f'metric_map_{now.strftime("%Y_%m_%d_%H_%M")}')
# plt.show()

def getzmodes(zmodeamps_osa, xx, yy):
    list_z = [0, 0, 0, 5, 4, 6, 9, 7, 8, 10, 15, 13, 11, 12, 14] #osa to noll indicies
    zmodeamps_noll = np.zeros(18)
    for i, zmodeamp in enumerate(zmodeamps_osa):
        zmodeamps_noll[list_z[i]] = zmodeamp

    z = zernike.Zernike(zmodeamps_noll)
    r = z.evalCartesian(xx, yy)
    return r


def getzmode(zmodenum, amp, xx, yy):
    zmodeamps_osa = [0, ] * 12
    zmodeamps_osa[zmodenum] = amp
    return getzmodes(zmodeamps_osa, xx, yy)

# r=getzmode(7, .5, xx, yy)
# plt.figure()
# plt.imshow(r)
# plt.show()

# new_mode = np.zeros()
# def getzmode(zmodenum, amp):
#     # cart = (modenum+4)
#     # L, K = 520, 520
#     # ddx = np.linspace(-1.0, 1.0, K)
#     # ddy = np.linspace(-1.0, 1.0, L)
#     # xv, yv = np.meshgrid(ddx, ddy)
#     # cart.make_cart_grid(xv, yv)
#     #
#     # c = np.zeros(cart.nk)
#     # plt.figure(1)
#     for i in range(stepnum):
#         plt.subplot(3, 3, i)
#         c *= 0.0
#         c[i] = 1.0
#         Phi = cart.eval_grid(c, matrix=True)
#         plt.imshow(Phi, origin='lower', extent=(-1, 1, -1, 1))
#         plt.axis('off')
#         new_mode = getzmode(modenum+4, step_amps[stepnum])
#     return(new_mode)


xdim, ydim = 256, 256
x = np.linspace(-1, 1, xdim)
xx,yy = np.meshgrid(x,x)

plt.figure()
step_amps = np.linspace(-.1, .1, metric_map.shape[1])
print(metric_map.shape)
previous_modes = np.zeros((xdim, ydim))
for modenum in range(metric_map.shape[0]):
    for stepnum in range(metric_map.shape[1]):
        # step = stepnum % 5
        # mode = np.floor(stepnum/5)
        # metric_map[stepnum]
        print(f"mode {modenum} step {stepnum} ")
        metric = metric_map[modenum, stepnum]
        new_mode = getzmode(modenum+4, step_amps[stepnum], xx, yy)
        plt.figure()
        plt.imshow(previous_modes + new_mode, vmin=-1, vmax=1)
        plt.colorbar()
        #plt.show()
        plt.savefig(f'metric_map_mode{modenum}_step{stepnum}')
    previous_modes += getzmode(modenum+4, step_amps[metric_map[modenum, :].argmax()], xx, yy)
