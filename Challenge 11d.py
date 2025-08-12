from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt

R = 3500
H = 5
FREQUENCIES = np.linspace(400, 750, 8)

# Find n for given frequency
def find_index_water(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

# Epsilon for primary rainbow
def primary_minimum(n): # RETURNS RADIANS
    angle = np.arcsin(((9 - n ** 2) / 8) ** 0.5)
    return np.pi - 6 * np.arcsin(np.sin(angle) / n) + 2 * angle

# Epsilon for secondary rainbow
def secondary_minimum(n): # RETURN RADIANS
    angle = np.arcsin(((4 - n ** 2) / 3) ** 0.5)
    return 4 * np.arcsin(angle / n) - 2 * angle

# Y coordinate for any given x coordinate with epsilon and alpha
def calc_y(px, eps, alpha): # NEEDS RADIANS
    radius = R * np.sin(eps) * np.cos(alpha)
    shift = radius - R * np.sin(eps - alpha) - H
    return (radius ** 2 - px ** 2) ** 0.5 - shift

# Maximum x before going below y-axis
def get_xlim(eps, alp): # NEEDS RADIANS
    return (R ** 2 * np.sin(eps - alp) * np.sin(eps + alp) + 
            2 * H * R * np.cos(eps) * np.sin(alp) - H ** 2) ** 0.5

# Maximum y (when x = 0)
def get_ylim(eps, alp): # NEEDS RADIANS
    return R * np.sin(eps - alp) + H

def get_radius(eps, alp): # NEEDS RADIANS
    return R * np.sin(eps) * np.cos(alp)

def get_shift(eps, alp): # NEEDS RADIANS
    return R * np.sin(eps) * np.cos(alp) - R * np.sin(eps - alp) - H

def choose_colour(freq):
    if freq < 405:
        return [np.nan, np.nan, np.nan]                     # Lower than red
    elif freq < 480:
        return [(freq-405)/75,0,0]                          # Red
    elif freq < 510:
        return [1, ((freq-480)/30)*127/255, 0]              # Orange
    elif freq < 530:
        return [1, 127/255 + ((freq-510)/20)*128/255, 0]    # Yellow
    elif freq < 600:
        return [1-(freq-530)/70, 1, 0]                      # Green
    elif freq < 620:
        return [0, 1, (freq-600)/20]                        # Cyan    
    elif freq < 680:
        return [0, 1-(freq-620)/60, 1]                      # Blue
    elif freq < 790:
        return [((freq-680)/110)*127/255, 0, 1]             # Violet
    else:
        return [np.nan, np.nan, np.nan]                     # Higher than violet

def plot_curve(freq, alpha): # alpha in RADIANS
    colour = choose_colour(freq)        # Colour of specified line based on freq
    n = find_index_water(freq)          # Refractive index
    print(n)
    eps1 = primary_minimum(n)           # Epsilon for primary
    eps2 = secondary_minimum(n)         # Epsilon for secondary
    print(eps1, eps2, alpha)
    x_limit1 = get_xlim(eps1, alpha)    # X limits for primary rainbow
    print(x_limit1)
    x_limit2 =  get_xlim(eps2, alpha)   # X limits for secondary rainbow
    print(x_limit2)

    draw_circle(eps1, alpha, colour)
    draw_circle(eps2, alpha, colour)

    # x_coords1 = np.linspace(-x_limit1, x_limit1, 1000)  # X coords above y-axis for primary
    # x_coords2 = np.linspace(-x_limit2, x_limit2, 1000)  # X coords above y-axis for secondary
    # y_coords1 = calc_y(x_coords1, eps1, alpha)          # Y coords for primary
    # y_coords2 = calc_y(x_coords2, eps2, alpha)          # Y coords for secondary
    # ax.plot(x_coords1, y_coords1, color = colour, linewidth = 1, label = "Primary")
    # ax.plot(x_coords2, y_coords2, color = colour, linewidth = 1, label = "Secondary")

def draw_circle(eps, alp, colour):
    centre_x = 0
    centre_y = -(R * np.sin(eps) * np.cos(alp) - R * np.sin(eps - alp) - H)
    radius = R * np.sin(eps) * np.cos(alp)
    theta = np.linspace(0, np.pi, 100)
    x = centre_x + radius * np.cos(theta)
    y = centre_y + radius * np.sin(theta)
    mask = y >= 0
    x = x[mask]
    y = y[mask]
    ax.plot(x, y, color = colour, linewidth=1)

def plot_rainbows(solar_angle): # Solar angle in RADIANS
    global ax
    max_freq = FREQUENCIES.max()
    n = find_index_water(max_freq)
    max_eps = secondary_minimum(n)
    print("Max elevation: ", max_eps)
    x_max = get_xlim(max_eps, solar_angle)
    print("X-axis limit: ", x_max)
    y_max = get_ylim(max_eps, solar_angle)
    print("Y-axis limit: ", y_max)
    ax.set_xlim = (-x_max*1.1, x_max*1.1)
    ax.set_ylim = (0, y_max * 1.1)

    for freq in FREQUENCIES:
        plot_curve(freq, solar_angle)

def update(val):
    global ax
    solar_angle = np.deg2rad(solar_slider.val)
    ax.clear()
    ax.set_title("Primary and Secondary Rainbows")
    max_freq = FREQUENCIES.max()
    n = find_index_water(max_freq)
    max_eps = secondary_minimum(n)
    print("Max elevation: ", max_eps)
    x_max = get_xlim(max_eps, solar_angle)
    print("X-axis limit: ", x_max)
    y_max = get_ylim(max_eps, solar_angle)
    print("Y-axis limit: ", y_max)
    ax.set_xlim = (-x_max*1.1, x_max*1.1)
    ax.set_ylim = (0, y_max * 1.1)

    #ax.set_xticks([])
    #ax.set_yticks([])

    plot_rainbows(solar_angle)

# Initialise plot
# def run_plot():
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.set_title("Primary and Secondary Rainbows")
x_limit = 500
y_limit = 100
ax.set_xlim(-x_limit, x_limit)
ax.set_ylim(0, y_limit)
ax.set_aspect('equal')
#ax.set_xticks([])
#ax.set_yticks([])
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)

# Slider
solar_angle = 5
solar_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
solar_slider = Slider(solar_ax, 'Solar Angle', 5, 50, valinit=solar_angle, valstep=1)

plot_rainbows(np.deg2rad(solar_angle))

solar_slider.on_changed(update)
plt.show()


