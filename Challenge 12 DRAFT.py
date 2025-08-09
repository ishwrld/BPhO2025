import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.bottom'] = False

prism_x = [0, 0.5, 1, 0]
prism_y = [0, np.sqrt(3)/2, 0, 0]

incident_x = [-0.5, 0]
incident_y = [0, (np.sqrt(3)/2)/2]

fig = plt.figure(facecolor='black')
ax = fig.add_subplot(111, facecolor='black')

ax.plot(prism_x, prism_y, color="white")
ax.plot(incident_x, incident_y, color="gainsboro")

ax.set_xticks([])
ax.set_yticks([])

ax.legend(facecolor='black')

plt.show()

