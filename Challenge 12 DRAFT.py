import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

alpha_init = 60
theta_init = 30
n = 1.5

fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')
plt.subplots_adjust(bottom=0.35)

theta_incidence = theta_init

def draw_triangle(alpha, theta_i):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    beta = (180 - alpha) / 2
    beta_rad = np.deg2rad(beta)

    base_length = 2
    half_base = base_length / 2
    height = half_base / np.tan(beta_rad)

    apex = np.array([0, height])
    left_base = np.array([-half_base, 0])
    right_base = np.array([half_base, 0])

    ax.plot(
        [left_base[0], apex[0], right_base[0], left_base[0]],
        [left_base[1], apex[1], right_base[1], left_base[1]],
        color="white"
    )

    midpoint = (apex + left_base) / 2

    side_vec = left_base - apex
    normal_vec = np.array([side_vec[1], -side_vec[0]])
    normal_vec = normal_vec / np.linalg.norm(normal_vec)


    normal_length = 0.4
    p_normal_start = midpoint - normal_vec * normal_length / 2
    p_normal_end = midpoint + normal_vec * normal_length / 2
    ax.plot([p_normal_start[0], p_normal_end[0]],
            [p_normal_start[1], p_normal_end[1]],
            linestyle=':', color='white')

    theta_rad = np.deg2rad(theta_i)
    incident_vec = (
        np.cos(theta_rad) * normal_vec
        + np.sin(theta_rad) * np.array([-normal_vec[1], normal_vec[0]])
    )

    length = 0.5
    p1 = midpoint + incident_vec * length
    p2 = midpoint
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="cyan")

    theta_i_rad = np.deg2rad(theta_i)
    alpha_rad = np.deg2rad(alpha)

    theta_t_rad = np.arcsin(
        np.sqrt(n**2 - np.sin(theta_i_rad)**2) * np.sin(alpha_rad)
        - np.sin(theta_i_rad) * np.cos(alpha_rad)
    )
    theta_t = np.rad2deg(theta_t_rad)

    delta = theta_i + theta_t - alpha

    delta1 = theta_i - (np.arcsin((1*np.sin(theta_i))/n))
    delta2 = delta - delta1

    

    ax.set_title(f"Theta = {theta_i:.1f} , Alpha = {alpha:.1f}", color="white")

draw_triangle(alpha_init, theta_init)

ax_slider_alpha = plt.axes([0.2, 0.18, 0.6, 0.03], facecolor="gray")
slider_alpha = Slider(ax_slider_alpha, 'Alpha', 60, 150, valinit=alpha_init, valstep=5)
slider_alpha.label.set_color('white')

ax_slider_theta = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor="gray")
slider_theta = Slider(ax_slider_theta, 'Theta', 10, 80, valinit=theta_init, valstep=5)
slider_theta.label.set_color('white')

def update(val):
    global theta_incidence
    theta_incidence = slider_theta.val
    draw_triangle(slider_alpha.val, theta_incidence)
    fig.canvas.draw_idle()

slider_alpha.on_changed(update)
slider_theta.on_changed(update)

plt.show()
