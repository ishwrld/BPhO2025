from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

C = 345
n = 1
y = 1
L0 = 2

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.title("Fermat's Principle of Least Time")
plt.xlabel("Distance (m)")
plt.ylabel("Time (s)")

def getAngle(x):
    return "θ = " + str(round(abs(np.degrees(np.arctan(x/y))),2))

x = np.linspace(0, L0, 1000)
t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L0 - x)**2 + y**2) / (C/n)
line, = ax.plot(x, t, lw=2)
lowest, = ax.plot(x[np.argmin(t)], np.min(t), marker="x", ms=7, lw = 2, color="red")
ax.set_xlim(0, L0)
ax.set_ylim(t.min() - t.min()**2 , t.max())

ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Length L', 1, 5, valinit=L0, valstep=0.1)
text = ax.text(0.8, 1.025, getAngle(x[np.argmin(t)]),
               fontsize=12,
               transform=ax.transAxes
               )


def update(val):
    L = slider.val
    x = np.linspace(0, L, 1000)
    t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L - x)**2 + y**2) / (C/n)
    line.set_data(x, t)
    ax.set_xlim(0, L)
    ax.set_ylim(t.min() - t.min()**2, t.max())
    lowest.set_data([x[np.argmin(t)]],[np.min(t)])
    text.set_text(getAngle(x[np.argmin(t)]))
    
    fig.canvas.draw_idle()
    #fig.canvas.flush_events()

slider.on_changed(update)
plt.show()
