import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False

prism_x = [0, 0.5, 1, 0]
prism_y = [0, np.sqrt(3)/2, 0, 0]

plt.figure()
plt.plot(prism_x, prism_y)


plt.xticks([])
plt.yticks([])

plt.show()
