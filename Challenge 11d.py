
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt

X_LIMIT = 500
Y_LIMIT = 100
R = 200

# Find n for given frequency
def formula(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

# Epsilon for primary rainbow
def primaryMinimum(n):
    angle = np.rad2deg(np.arcsin(((9 - n ** 2) / 8) ** 0.5))
    return 180 - 6 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) + 2 * angle

# Epsilon for secondary rainbow
def secondaryMinimum(n):
    angle = np.rad2deg(np.arcsin(((4 - n ** 2) / 3) ** 0.5))
    return 4 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) - 2 * angle

# Y coordinate for any given x coordinate with epsilon and alpha
def calcY(px, eps, alpha):
    return (eps ** 2 - px ** 2) ** 0.5 - alpha

def chooseColour(freq):
    if freq < 405:  # Lower than red
        return [np.nan, np.nan, np.nan]
    elif freq < 480:
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

def plotCurve(freq, alpha):
    # x ** 2 + (y + alp) ** 2 = eps ** 2
    # radius = R * np.sin(eps) * np.cos(alp)
    # minY = radius - R * np.sin(eps - alp) - 4
    colour = chooseColour(freq)
    n = formula(freq)
    eps1 = primaryMinimum(n)
    eps2 = secondaryMinimum(n)
    x_coords = np.linspace(-X_LIMIT,X_LIMIT, 1000)
    y_coords1 = calcY(x_coords, eps1, alpha)
    y_coords2 = calcY(x_coords, eps2, alpha)
    ax.plot(x_coords, y_coords1, color = colour, linewidth = 1, label = "Primary")
    ax.plot(x_coords, y_coords2, color = colour, linewidth = 1, label = "Secondary")


def update(val):
    solar_angle = np.deg2rad(solar_slider.val)
    ax.clear()
    ax.set_title("Primary and Secondary Rainbows")
    ax.set_ylim(0, Y_LIMIT)
    ax.set_aspect('equal')
    #ax.set_xticks([])
    #ax.set_yticks([])
    for freq in frequencies:
        plotCurve(freq, solar_angle)


# Initialise plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.set_title("Primary and Secondary Rainbows")
#ax.set_xlim(-X_LIMIT, X_LIMIT)
ax.set_ylim(0, Y_LIMIT)
ax.set_aspect('equal')
#ax.set_xticks([])
#ax.set_yticks([])
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)

# Slider
solar_angle = 5
solar_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
solar_slider = Slider(solar_ax, 'Solar Angle', 0, 180, valinit=solar_angle, valstep=1)

frequencies = np.linspace(400, 750, 7)
print(frequencies)
for freq in frequencies:
    plotCurve(freq, np.deg2rad(solar_angle))




# indexes = formula(frequencies)
# primaryElevation = primaryMinimum(indexes)
# secondaryElevation = secondaryMinimum(indexes)
# colour = np.array([chooseColour(f) for f in frequencies])
solar_slider.on_changed(update)
plt.show()