import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

LW = 0.5
FREQUENCIES = np.linspace(410, 750, 15)

def findIndexWater(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

def secondaryElevation(n):
    angle = np.arcsin(((9 - n ** 2) / 8) ** 0.5)
    return np.pi - 6 * np.arcsin(np.sin(angle) / n) + 2 * angle

def primaryElevation(n):
    angle = np.arcsin(((4 - n ** 2) / 3) ** 0.5)
    return 4 * np.arcsin(np.sin(angle) / n) - 2 * angle

def chooseColour(freq):
    if freq < 405:  # Lower than red
        return [np.nan, np.nan, np.nan]
    if freq < 480:
        return [(freq-405)/75,0,0]  # Red
    elif freq < 510:
        return [1, ((freq-480)/30)*127/255, 0]  # Orange
    elif freq < 530:
        return [1, 127/255 + ((freq-510)/20)*128/255, 0]  # Yellow
    elif freq < 600:
        return [1-(freq-530)/70, 1, 0]  # Green
    elif freq < 620:
        return [0, 1, (freq-600)/20]  # Cyan    
    elif freq < 680:
        return [0, 1-(freq-620)/60, 1]  # Blue
    elif freq < 790:
        return [((freq-680)/110)*127/255, 0, 1]  # Violet
    else:
        return [np.nan, np.nan, np.nan]

def drawCurve(freq, alpha):
    colour = chooseColour(freq)
    n = findIndexWater(freq)
    eps1 = primaryElevation(n)
    eps2 = secondaryElevation(n)

    x1, y1 = getCircleCoords(eps1, alpha) # Primary
    x2, y2 = getCircleCoords(eps2, alpha) # Secondary

    ax.plot(x1, y1, color = colour, linewidth = LW)
    ax.plot(x2, y2, color = colour, linewidth = LW)

def getCircleCoords(eps, alp):
    theta = np.linspace(0, 2 * np.pi, 360)
    radius = range * np.sin(eps) * np.cos(alp)
    centre_y = -(range * np.sin(eps) * np.cos(alp) - range * np.sin(eps - alp) - height)
    # range * np.sin(eps - alp) + height - range * np.sin(eps) * np.cos(alp)
    x = radius * np.cos(theta)
    y = centre_y + radius * np.sin(theta)
    mask = y >= 0
    x = x[mask]
    y = y[mask]
    return x, y    

def drawRainbows(solar_angle):
    for freq in FREQUENCIES:
        drawCurve(freq, solar_angle)

def findLimits(solar_angle):
    # Set axis limits using max frequency
    max_freq = FREQUENCIES.max()
    n = findIndexWater(max_freq)
    eps2 = secondaryElevation(n)
    x_coords, y_coords = getCircleCoords(eps2, solar_angle)
    return x_coords.max(), y_coords.max()

def update(val):
    # global height, range
    solar_deg = solar_slider.val
    solar_rad = np.deg2rad(solar_deg)
    # height = height_slider.val
    # range = range_slider.val
    ax.clear()
    ax.set_title("Primary and Secondary Rainbows")
    x_lim, y_lim = findLimits(solar_rad)
    ax.set_xlim(-x_lim*1.1, x_lim*1.1)
    ax.set_ylim(0, x_lim*1.1)
    ax.set_xticks([])
    ax.set_yticks([])
    
    drawRainbows(solar_rad)

# Initiliase plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom = 0.25) # Give space for slider
ax.set_title("Primary and Secondary Rainbows")
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False) # Make all border invisible

# Slider
initAngle = 5
solar_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
solar_slider = Slider(solar_ax, "Solar Angle, α", 1, 45, valinit = initAngle, valstep=0.25)

# Left slider for range. R
range = 3500
# range_ax_left = plt.axes([0.075, 0.25, 0.03, 0.65])
# range_slider = Slider(range_ax_left, "Range, r", 0, 5000, valinit = range, orientation='vertical')

# Right slider for height, H
height = 5
# height_ax_right = plt.axes([0.91, 0.25, 0.03, 0.65]) # (left, bottom, width, height)
# height_slider = Slider(height_ax_right, "Height, h", 0, 100, valinit = height, orientation='vertical')

# Set limits
x_lim, y_lim = findLimits(np.deg2rad(initAngle))
ax.set_xlim(-x_lim*1.1, x_lim*1.1)
ax.set_ylim(0, x_lim*1.1)

# Draw rainbow
drawRainbows(np.deg2rad(initAngle))

solar_slider.on_changed(update)
# range_slider.on_changed(update)
# height_slider.on_changed(update)

plt.show()