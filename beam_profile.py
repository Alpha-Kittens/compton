import os
from data_loader import read_data
import matplotlib.pyplot as plt

folder = 'data/21 November/Beam_profile/'

files = os.listdir(folder)

cpss = []
angles = []
for file_name in files:
    fp = folder + file_name

    data = read_data(fp)

    print(data['counts'])

    cps = data['counts']/(data['time'].val)

    print(cps)
    angle = data['angle']

    cpss.append(cps)
    angles.append(angle)

plt.plot(angles, cpss)
plt.show()
