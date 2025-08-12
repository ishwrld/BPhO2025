import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

FREQUENCIES = np.linspace(410, 750, 15)
HEIGHT = 2
NORM_LEN = 0.3
INCIDENT_LENGTH = 1
EXIT_LENGTH = 1
LW = 0.5 # line width

def refractiveGlass(freq): # Returns n, refractive index
    wavelength = 3e8 / (freq * 1e6)
    # Sellmeier coefficients for crown glass
    coeffA = [1.03961212, 0.231792344, 1.01146945]
    coeffB = [0.00600069867, 0.0200179144, 103.560653]

    #wavelength = wavelength / 1000  # Convert to micrometres
    waveSquare = wavelength ** 2  # Wavelength squared (makes equation easier)
    sumCoeff = 0
    for index in range(len(coeffA)):
        sumCoeff += (coeffA[index] * waveSquare) / (waveSquare - coeffB[index])

    return (1 + sumCoeff) ** 0.5

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

def sin(angle): # DEGREES INPUT
    return np.sin(np.deg2rad(angle))

def cos(angle): # DEGREES INPUT
    return np.cos(np.deg2rad(angle))

def tan(angle): # DEGREES INPUT
    return np.tan(np.deg2rad(angle))

def get_theta_t(alpha, theta_i, n):
    return np.rad2deg(np.arcsin((n ** 2 - sin(theta_i) ** 2) ** 0.5 * sin(alpha)
                                 - sin(theta_i) * cos(alpha)))

def get_half_length(alpha):
    return 0.5 * HEIGHT / sin(90 - alpha / 2)

def get_exit_coord(alpha, theta_i, n): # Coordinates of exit point
    global HEIGHT
    delta = np.rad2deg(np.arcsin(sin(theta_i)/n))
    side_a = get_half_length(alpha)
    angle_a = 90 + delta - alpha
    angle_b = 90 - delta
    side_b = side_a * sin(angle_b) / sin(angle_a)
    x_coord = side_b * sin(alpha / 2)
    y_coord = HEIGHT - side_b * cos(alpha / 2)
    return x_coord, y_coord

def draw_triangle(alpha):
    global HEIGHT, NORM_LEN

    base_half = HEIGHT * tan(alpha/2)
    left_point = np.array([-base_half, 0])
    right_point = np.array([base_half, 0])
    apex = np.array([0, HEIGHT])

    ax.plot(
        [left_point[0], apex[0], right_point[0], left_point[0]],
        [left_point[1], apex[1], right_point[1], left_point[1]],
        color = 'white', linewidth = LW
    )

    midpoint = (left_point + apex) / 2
    gradient_angle1 = alpha / 2
    normal1_start = [midpoint[0] - NORM_LEN * cos(gradient_angle1),
                    midpoint[1] + NORM_LEN * sin(gradient_angle1)]
    normal1_end = [midpoint[0] + NORM_LEN * cos(gradient_angle1),
                    midpoint[1] - NORM_LEN * sin(gradient_angle1)]
    
    ax.plot([normal1_end[0], normal1_start[0]], [normal1_end[1], normal1_start[1]], 
            linestyle = ':', color = 'white', linewidth = LW)

def draw_incident_ray(alpha, theta_i):
    global HEIGHT, INCIDENT_LENGTH

    base_half = HEIGHT * tan(alpha/2)
    midpoint = [-base_half / 2, HEIGHT / 2]
    grad_angle = theta_i - alpha / 2
    incident_start = [midpoint[0] - INCIDENT_LENGTH * cos(abs(grad_angle)),
                      midpoint[1] - INCIDENT_LENGTH * sin(grad_angle)]
    
    ax.plot([midpoint[0], incident_start[0]], [midpoint[1], incident_start[1]], 
            linestyle = '-', color = 'white', linewidth = LW)

def draw_refracted_ray(alpha, theta_i, theta_t, colour,n):
    global HEIGHT, EXIT_LENGTH
    # Refracted ray
    base_half = HEIGHT * tan(alpha/2)
    midpoint = [-base_half / 2, HEIGHT / 2]
    x_exit, y_exit = get_exit_coord(alpha, theta_i,n)
    delta = np.rad2deg(np.arcsin(sin(theta_i)/n))
    final_grad_angle = 90 + alpha / 2 - theta_t
    x_final = x_exit + EXIT_LENGTH * sin(final_grad_angle)
    y_final = y_exit - EXIT_LENGTH * cos(final_grad_angle)
    ax.plot([midpoint[0], x_exit, x_final], [midpoint[1], y_exit, y_final], color = colour, linewidth = LW)
    # Normal line
    exit_point = get_exit_coord(alpha, theta_i, n)
    gradient_angle2 = alpha / 2
    normal1_start = [exit_point[0] + NORM_LEN * cos(gradient_angle2),
                    exit_point[1] + NORM_LEN * sin(gradient_angle2)]
    normal1_end = [exit_point[0] - NORM_LEN * cos(gradient_angle2),
                    exit_point[1] - NORM_LEN * sin(gradient_angle2)]
    ax.plot([normal1_end[0], normal1_start[0]], [normal1_end[1], normal1_start[1]], 
            linestyle = ':', color = 'white', linewidth = LW)

def draw_multi_rays(alpha, theta_i):
    for freq in FREQUENCIES:
        n = refractiveGlass(freq)
        colour = chooseColour(freq)
        theta_t = get_theta_t(alpha, theta_i, n)
        draw_refracted_ray(alpha, theta_i, theta_t, colour,n)

def update(val):
    theta_incidence = slider_theta.val
    alpha = slider_alpha.val
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.set_title(f"Theta = {theta_incidence:.1f} , Alpha = {alpha:.1f}", color="white")
    draw_triangle(alpha)
    draw_incident_ray(alpha, theta_incidence)
    draw_multi_rays(alpha, theta_incidence)
    fig.canvas.draw_idle()

alpha_init = 45
theta_init = 7

fig, ax = plt.subplots(facecolor = 'black')
ax.set_title(f"Theta = {theta_init:.1f} , Alpha = {alpha_init:.1f}", color='white')
ax.set_facecolor('black')
ax.set_aspect('equal')
plt.subplots_adjust(bottom = 0.35)

# Alpha slider
ax_slider_alpha = plt.axes([0.2, 0.18, 0.6, 0.03], facecolor='gray')
slider_alpha = Slider(ax_slider_alpha, "Alpha", 5, 60, valinit=alpha_init, valstep=1)
slider_alpha.label.set_color('white')

# Theta slider
ax_slider_theta = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='gray')
slider_theta = Slider(ax_slider_theta, "Theta", 0, 90, valinit=theta_init, valstep=1)
slider_theta.label.set_color('white')

draw_triangle(alpha_init)
draw_incident_ray(alpha_init, theta_init)
draw_multi_rays(alpha_init, theta_init)

slider_alpha.on_changed(update)
slider_theta.on_changed(update)

manager = plt.get_current_fig_manager()
manager.toolbar.pack_forget()  # Removes toolbar from Tkinter window
plt.show()