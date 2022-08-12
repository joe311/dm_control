import numpy as np
from skimage import io
from matplotlib import pyplot as plt
tifpath = r'E:\SLM\baseline2_PSF_scanphasecorrected_0pt2beads_0.23step_10fames_40slices_30power_31zoom_zstack_00001.tif'

data = io.imread(tifpath).mean(axis=1)
print(data.shape)

plt.figure()
# plt.imshow(data[10, ...])
#plt.imshow(data[:, 260, :], aspect='equal', extent=[0, 512*0.032, 0, 10*0.23])# aspect=0.89/0.032
plt.imshow(data[20, :], aspect='equal', extent=[0, 512*0.032, 0, 10*0.23])# aspect=0.89/0.032
plt.ylabel('Z')
plt.xlabel('X')
plt.show()

plt.figure()
plt.imshow(data[10, ...], aspect='equal', extent=[0, 512*0.032, 0, 512*0.032])
#plt.imshow(data[:, 260, :], aspect='equal', extent=[0, 512*0.032, 0, 10*0.89])# aspect=0.89/0.032
plt.ylabel('Y')
plt.xlabel('X')
plt.show()

print()