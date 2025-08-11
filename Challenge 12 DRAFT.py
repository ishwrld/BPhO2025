import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

alpha_init = 80
theta_init = 30

fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')
plt.subplots_adjust(bottom=0.35)

theta_incidence = theta_init

def draw_triangle(alpha, theta):
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

    apex = (0, height)
    left_base = (-half_base, 0)
    right_base = (half_base, 0)

    ax.plot(
        [left_base[0], apex[0], right_base[0], left_base[0]],
        [left_base[1], apex[1], right_base[1], left_base[1]],
        color="white"
    )

    ax.set_title(f"Theta = {theta} , Alpha = {alpha}", color="white")

draw_triangle(alpha_init, theta_init)

ax_slider_alpha = plt.axes([0.2, 0.18, 0.6, 0.03], facecolor="gray")
slider_alpha = Slider(ax_slider_alpha, 'Alpha', 45, 150, valinit=alpha_init, valstep=5)
slider_alpha.label.set_color('white')

ax_slider_theta = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor="gray")
slider_theta = Slider(ax_slider_theta, 'Theta', 10, 90, valinit=theta_init, valstep=5)
slider_theta.label.set_color('white')

def update(val):
    global theta_incidence
    theta_incidence = slider_theta.val
    draw_triangle(slider_alpha.val, theta_incidence)
    fig.canvas.draw_idle()

slider_alpha.on_changed(update)
slider_theta.on_changed(update)

plt.show()
