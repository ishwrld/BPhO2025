from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

C = 345
n = 1
n2 = 1.5
y = 1
L0 = 2

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.title("Test for Snell's Law")
plt.xlabel("Distance (m)")
plt.ylabel("Time (s)")

x = np.linspace(0, L0, 1000)
t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L0 - x)**2 + y**2) / (C/n2)
line, = ax.plot(x, t, lw=2)
ax.set_xlim(0, L0)
ax.set_ylim(t.min() - t.min()**2, t.max())

ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Length L', 1, 5, valinit=L0, valstep=0.5)

def update(val):
    L = slider.val
    x = np.linspace(0, L, 1000)
    t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L - x)**2 + y**2) / (C/n2)
    line.set_data(x, t)
    ax.set_xlim(0, L)
    ax.set_ylim(t.min() - t.min()**2, t.max())
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
