from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import math


C = 345
n = 1
y = 1
L = 2
x = np.linspace(0, L, 1000)

def formula(x):
    return (np.sqrt((x)**2 + y**2) / (C/n)) + (np.sqrt((L - x)**2 + y**2) / (C/n))

def update(val):
    global L, x
    L = length_Slider.val
    x = np.linspace(0, L, 1000)
    line.set_xdata(x)
    line.set_ydata(formula(x))
    ax.set_xlim(0, L)
    ax.set_ylim(0, max(formula(x)))
    plot1.canvas.draw_idle()

ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
length_Slider = Slider(ax_slider, 'Change Length', 1, 5.0, valinit=4)

t = formula(x)

plot1, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = ax.plot(x, t, linestyle='-', color='b', label='Data Points')

length_Slider.on_changed(update)

plt.show()

