import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

alpha_init = 60

fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')
plt.subplots_adjust(bottom=0.25)

def draw_triangle(alpha):
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

    ax.set_title(f"Theta = filler , Alpha = {alpha}", color="white")

draw_triangle(alpha_init)

ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor="gray")
slider_alpha = Slider(ax_slider, 'Alpha', 60, 150, valinit=alpha_init, valstep=5)
slider_alpha.label.set_color('white')  # make label visible

def update(val):
    draw_triangle(slider_alpha.val)
    fig.canvas.draw_idle()

slider_alpha.on_changed(update)

plt.show()




