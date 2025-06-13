import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

fig, ax = plt.subplots()

ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.axvline(x=0, color='purple', linestyle='--', linewidth=1.5)
plt.title("Reflection in a Plane Mirror")
ax.text(2.2, 3, "Object", color='red', fontsize=12)
ax.text(-4.25, 3, "Virtual Image", color='green', fontsize=12)
ax.grid(True, linestyle=':')

image_path = r"Einstein.jpg"
img = Image.open(image_path)
img_array = np.array(img)
virtual_img_array = np.fliplr(img_array)

virtual_ex = [-5, -1, -2, 2]
real_ex = [1, 5, -2, 2]

virtual_image = ax.imshow(virtual_img_array, extent=virtual_ex, zorder=1)
real_image = ax.imshow(img_array, extent=real_ex, zorder=1)

dragging = False

def on_press(event):
    global dragging
    contains, _ = real_image.contains(event)
    if contains:
        dragging = True

def on_release(event):
    global dragging
    dragging = False

def on_motion(event):
    global virtual_ex, real_ex
    if dragging:
        width = real_ex[1] - real_ex[0]
        height = real_ex[3] - real_ex[2]
        dx = event.xdata
        dy = event.ydata

        real_ex = [
            dx - width/2,
            dx + width/2,
            dy - height/2,
            dy + height/2
        ]
        real_image.set_extent(real_ex)

        virtual_ex = [
            -real_ex[1],
            -real_ex[0],
            real_ex[2],
            real_ex[3]
        ]
        virtual_image.set_extent(virtual_ex)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)


plt.show()
