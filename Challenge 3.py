from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import math

C = 345 
n = 1
y = 1
L = 2


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25) 
 # Adjust space for sliders

x = np.linspace(0, L, 1000) #Plotting on x
t = np.sqrt((x)**2 + y**2) / (C/n)+ np.sqrt((L - x)**2 + y**2) / (C/n) 
#Plotting on y

line, = plt.plot(x, t, lw=2)
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='purple')
slider = Slider(ax_slider, 'Length', 1, 5, valinit=L, valstep=0.5)

def update(val):
    L = slider.val
    line.set_ydata(np.sqrt((x)**2 + y**2) / (C/n) + np.sqrt((L - x)**2 + y**2) / (C/n))
    line.set_xdata(x)
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()
