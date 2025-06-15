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

fig, (ax, ax2) = plt.subplots(1,2)
plt.subplots_adjust(bottom=0.25)

def getAngle(angle, opp,hyp):
    return angle + " = " + str(round(abs(np.degrees(np.arctan(opp/hyp))),2))

ax.set_title("Snell's Law")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Time (s)")

x = np.linspace(0, L, 1000)
t = np.sqrt(x**2 + y**2) / c1 + np.sqrt((L - x)**2 + Y**2) / c2
line, = ax.plot(x, t, lw=2)
lowest, = ax.plot(x[np.argmin(t)], np.min(t), marker="x", ms=7, lw = 2, color="red")
ax.set_xlim(0, L)
ax.set_ylim(t.min() - t.min()**2, t.max())

ax1_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
c1_slider = Slider(ax1_slider, 'c1 (m/s)', 5, 1000, valinit=345, valstep=5)

ax2_slider = plt.axes([0.2, 0, 0.65, 0.03])
c2_slider = Slider(ax2_slider, 'c2 (m/s)', 5, 1000, valinit=230, valstep=5)

ax2.set_title(f"c1 = {np.round(c1)}m/s c2 = {np.round(c2)}m/s")
ax2.spines['bottom'].set_position(('data', 0))
ray, = ax2.plot([0, x[np.argmin(t)], L], [y, 0, -Y])
normal = ax2.axvline(x=x[np.argmin(t)], color='black', linestyle='--', linewidth=1.5)

text1 = ax2.text(0.05, 0, getAngle("θ", x[np.argmin(t)], y),
               fontsize=12, transform=ax2.transAxes, ha = "left", va = "bottom")
text2 = ax2.text(0.045, 0.08, getAngle("Φ",L-x[np.argmin(t)], -Y),
               fontsize=12, transform=ax2.transAxes, ha = "left", va = "bottom")
ax2.set_xlim(0, L)
ax2.set_ylim(-Y,y)

def update(val):
    c1 = c1_slider.val
    c2 = c2_slider.val
    x = np.linspace(0, L, 1000)
    t = np.sqrt(x**2 + y**2) / c1 + np.sqrt((L - x)**2 + Y**2) / c2
    line.set_data(x, t)
    ax.set_xlim(0, L)
    ax.set_ylim(t.min() - t.min()**2, t.max())
    lowest.set_data([x[np.argmin(t)]],[np.min(t)])
    text1.set_text(getAngle("θ", x[np.argmin(t)], y))
    text2.set_text(getAngle("Φ",L-x[np.argmin(t)], Y))
    ray.set_xdata([0, x[np.argmin(t)], L])
    normal.set_xdata([x[np.argmin(t)]])
    ax2.set_title(f"c1 = {np.round(c1)}m/s c2 = {np.round(c2)}m/s")
    fig.canvas.draw_idle()

c1_slider.on_changed(update)
c2_slider.on_changed(update)
plt.subplots_adjust(wspace=0.3)
plt.show()
