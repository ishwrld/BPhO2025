from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import math

C = 345
n = 1
y = 1

def update(val):
    global L
    L = length_Slider.val
    line.set_ydata(formula(x))
    plot1.canvas.draw_idle()

def formula(x):
    return (np.sqrt((x)**2 + y**2) / (C/n)) + (np.sqrt((L - x)**2 + y**2) / (C/n))

ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
length_Slider = Slider(ax_slider, 'Change Length', 1, 5.0, valinit=4)

plot1, plot2 = plt.subplots()
plt.subplots_adjust(bottom=0.25)
L = 2
x = np.linspace(0, L, 1000)
line, = plt.plot(x, formula(x), lw=1)

length_Slider.on_changed(update)

plt.show()
