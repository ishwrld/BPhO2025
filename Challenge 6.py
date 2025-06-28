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

ax.grid(True, linestyle=':')

image_path = r"Einstein.jpg"
img = Image.open(image_path)
img_array = np.array(img)
virtual_img_array = np.fliplr(img_array)

virtual_ex = [-5, -1, -2, 2]
real_ex = [1, 5, -2, 2]

virtual_image = ax.imshow(virtual_img_array, extent=virtual_ex, zorder=1)
real_image = ax.imshow(img_array, extent=real_ex, zorder=1)

objectTxt = ax.text(0.5*(real_ex[0]+real_ex[1]), real_ex[3]+0.6, "Object", color='red', fontsize=12,
                    ha = "center", va = "top")
virtualTxt = ax.text(0.5*(virtual_ex[0]+virtual_ex[1]), virtual_ex[3]+0.6, "Virtual Image",
                      color='green', fontsize=12,
                      ha = "center", va = "top")

# Lens height
lens_height = 7.5

# Parametric curve for left side of lens
theta = np.linspace(-np.pi/2, np.pi/2, 100)
x_left = -0.3 * np.cos(theta)
y_left = np.linspace(-lens_height/2, lens_height/2, 100)

# Parametric curve for right side of lens
x_right = 0.3 * np.cos(theta)
y_right = np.linspace(-lens_height/2, lens_height/2, 100)

# Plot left and right sides
ax.plot(x_left, y_left, color='blue')
ax.plot(x_right, y_right, color='blue')

# Optional: fill the lens
ax.fill_betweenx(y_left, x_left, x_right, color='skyblue', alpha=0.3)


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
        objectTxt.set_position([dx, real_ex[3]+0.6])

        virtual_ex = [
            -real_ex[1],
            -real_ex[0],
            real_ex[2],
            real_ex[3]
        ]
        virtual_image.set_extent(virtual_ex)
        virtualTxt.set_position([0.5*(virtual_ex[0]+virtual_ex[1]), virtual_ex[3]+0.6])



        fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)


plt.show()
