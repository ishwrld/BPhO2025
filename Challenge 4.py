from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

C = 345
n = 1
n2 = 1.5
y = 1
Y = 1
L = 2
c1 = 345
c2 = 230

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.title("Snell's Law")
plt.xlabel("Distance (m)")
plt.ylabel("Time (s)")

def getAngle(angle, opp,hyp):
    return angle + " = " + str(round(abs(np.degrees(np.arctan(opp/hyp))),2))

x = np.linspace(0, L0, 1000)
t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L0 - x)**2 + Y**2) / (C/n2)
line, = ax.plot(x, t, lw=2)
lowest, = ax.plot(x[np.argmin(t)], np.min(t), marker="x", ms=7, lw = 2, color="red")
ax.set_xlim(0, L0)
ax.set_ylim(t.min() - t.min()**2, t.max())

ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Length L', 1, 5, valinit=L0, valstep=0.1)

text1 = ax.text(0.805, 1.125, getAngle("θ", x[np.argmin(t)], y),
               fontsize=12,
               transform=ax.transAxes
               )
text2 = ax.text(0.8, 1.025, getAngle("Φ",L0-x[np.argmin(t)], Y),
               fontsize=12,
               transform=ax.transAxes
               )

def update(val):
    L = slider.val
    x = np.linspace(0, L, 1000)
    t = np.sqrt(x**2 + y**2) / (C/n) + np.sqrt((L - x)**2 + Y**2) / (C/n2)
    line.set_data(x, t)
    ax.set_xlim(0, L)
    ax.set_ylim(t.min() - t.min()**2, t.max())
    lowest.set_data([x[np.argmin(t)]],[np.min(t)])

    text1.set_text(getAngle("θ", x[np.argmin(t)], y))
    text2.set_text(getAngle("Φ",L0-x[np.argmin(t)], Y))
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
