# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# def challenge_6BROKEN():
#     # Load image and convert to RGB
#     img = cv2.imread('Einstein.jpg')
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     h, w = img.shape[:2]

#     # Create meshgrid of (x, y) coordinates
#     x_coords, y_coords = np.meshgrid(np.arange(w), np.arange(h))

#     # Define focal length
#     f = 500.0  # Change this value as needed

#     # Avoid division by zero
#     x_safe = np.where((x_coords - f) == 0, 1e-6, x_coords - f)

#     # Apply custom mapping
#     X = -f * x_coords / x_safe
#     Y = y_coords * X / x_coords

#     # Handle division by zero for x_coords
#     X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
#     Y = np.nan_to_num(Y, nan=0.0, posinf=0.0, neginf=0.0)

#     # Ensure maps are float32 for remap()
#     map_x = X.astype(np.float32)
#     map_y = Y.astype(np.float32)

#     # Apply remapping
#     remapped = cv2.remap(
#         img_rgb,
#         map_x,
#         map_y,
#         interpolation=cv2.INTER_LINEAR,
#         borderMode=cv2.BORDER_CONSTANT,
#         borderValue=(255, 255, 255)  # White in RGB
#     )
#     # Plot results
#     fig, axes = plt.subplots(1, 2, figsize=(10, 5))
#     axes[0].imshow(img_rgb)
#     axes[0].set_title("Original")
#     axes[0].axis("off")

#     axes[1].imshow(remapped)
#     axes[1].set_title("Custom Remapped")
#     axes[1].axis("off")

#     plt.tight_layout()
#     plt.show()


# def challenge_5(px,py): 
#     """
#     Function to flip the image horizontally for Challenge 5.
#     Args:
#         px (numpy.ndarray): x-coordinates of the image.
#         py (numpy.ndarray): y-coordinates of the image.
#     Returns:
#         tuple: New x and y coordinates after flipping.
#     """
#     new_x = -px #Flip image horizontally
#     new_y = py
    
#     # Ensure maps are float32 for remap()
#     map_x = new_x.astype(np.float32)
#     map_y = new_y.astype(np.float32)

#     return map_x, map_y

# def challenge_6(px,py): 
#     """
#     """
#     f = 0.5  # Focal length, adjust as needed
    
#     # Avoid division by zero
#     # x_safe = np.where((px - f) == 0, 1e-6, px - f)
    
#     new_x = -f * px / x_safe
#     new_y = py * new_x / px

#     # Handle division by zero for x_coords
#     # X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
#     # Y = np.nan_to_num(Y, nan=0.0, posinf=0.0, neginf=0.0)
    
#     # Ensure maps are float32 for remap()
#     map_x = new_x.astype(np.float32)
#     map_y = new_y.astype(np.float32)

#     return map_x, map_y

# def world_to_pixel(x_real, y_real):
#     """Maps real-world coordinates to image pixel indices."""
#     real_ex =[x_real.min(), x_real.max(), y_real.min(), y_real.max()]
    
#     x_pixel = (x_real - real_ex[0]) / (real_ex[1] - real_ex[0]) * (img_w - 1)
#     y_pixel = (real_ex[3] - y_real) / (real_ex[3] - real_ex[2]) * (img_h - 1)  # y-axis inverted
#     return x_pixel.astype(np.float32), y_pixel.astype(np.float32)


# image_path = r"Einstein.jpg"
# img = cv2.imread(image_path)
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# real_ex = [1, 5, -2, 2]
# #EXTENT = [left, right, bottom, top]]
# h = real_ex[3] - real_ex[2]
# w = real_ex[1] - real_ex[0]

# # Create meshgrid of (x, y) coordinates
# x, y = np.meshgrid(
#     np.arange(real_ex[0],real_ex[1], w),
#     np.arange(real_ex[2], real_ex[3], step=h/1000))

# X,Y = challenge_5(x, y) #Flip image horizontally

# map_x, map_y = world_to_pixel(X, Y, real_ex, (h, w))

# # Apply remapping
# remapped = cv2.remap(
#     img_rgb, map_x, map_y,
#     interpolation=cv2.INTER_LINEAR,
#     borderMode=cv2.BORDER_CONSTANT,
#     borderValue=(255, 0, 0)  # RED in RGB
#     )
# cv2.imshow("Remapped Image", remapped)

# # Plot results
# fig, ax = plt.subplots()
# ax.set_xlim(-6, 6)
# ax.set_ylim(-6, 6)
# ax.imshow(img_rgb, extent=real_ex)
# ax.imshow(remapped, extent=[X.min(), X.max(), Y.min(), Y.max()])

# print("x_coords:", X)
# print("y_coords:", Y)
# print("Shape of x_coords:", X.shape)
# print("Shape of y_coords:", Y.shape)

# plt.show()



# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Load Image
obj = plt.imread("Einstein.jpg")  # Put object into numpy array
H, W = obj.shape[:2]  # Get height and width (in pixels) of object image

# Constants
f = 500.0  # Focal length of thin lens

# Bounds for the object (prevent division by zero at x = f)
X_MIN = f / 2
X_MAX = 3*f
Y_MIN = -f
Y_MAX = f

# Initialise Variables
obj_x = f  # Initial object x position
obj_y = H/2  # Initial object y position
dragging = False

# Subprograms
def map_pixel(x_obj, y_obj):
    """
    Map an input pixel at (x_obj, y_obj) through an ideal thin lens of focal length f,
    returning (x_img, y_img).
    """
    x_img = -f * x_obj / (x_obj - f)
    y_img = (y_obj / x_obj) * x_img
    return x_img, y_img

# Interactive redraw

def redraw():
    """
    Clear and re‑draw the object, its warped image, the lens, and rays.
    """
    ax_67.clear()
    ax_67.set_xlim(-3*f, 3*f)
    ax_67.set_ylim(-1.5*f, 1.5*f)
    ax_67.set_aspect('equal')

    ax_67.set_title(f"Image of object in converging lens")
    ax_67.set_xlabel("x")
    ax_67.set_ylabel("y")
    ax_67.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Draw principal axis
    ax_67.axvline(0, linestyle='--', color='gray')
    ax_67.axhline(0, linestyle='--', color='gray')

    # Draw lens as an ellipse at x=0
    aperture = 400        # vertical span of the lens
    thickness = 0.2 * f   # horizontal thickness (for visual only)
    lens = Ellipse((0, 0), width=thickness, height=aperture,
                   edgecolor='blue', facecolor='none', linewidth=2)
    ax_67.add_patch(lens)

    # Plot both focal points
    ax_67.plot(f,  0, marker='x', color='black', markersize=8, linestyle='None', label='Foci')
    ax_67.plot(-f, 0, marker='x', color='black', markersize=8, linestyle='None')

    # Compute object image extent (scaled)
    scale = 0.5
    scaled_W = W * scale
    scaled_H = H * scale
    obj_extent = [
        obj_x - scaled_W/2,  # x min
        obj_x + scaled_W/2,  # x max
        obj_y - scaled_H,    # y min
        obj_y               # y max
    ]

    # Display Object image
    ax_67.imshow(obj, origin='upper', extent=obj_extent, zorder=1)

    # Compute warped image scatter
    x_vals = np.linspace(obj_extent[0], obj_extent[1], W)
    y_vals = np.linspace(obj_extent[2], obj_extent[3], H)
    x_obj_grid, y_obj_grid = np.meshgrid(x_vals, y_vals)

    x_img_grid, y_img_grid = map_pixel(x_obj_grid, y_obj_grid)

    x_flat = x_img_grid.ravel()
    y_flat = y_img_grid.ravel()
    colours = obj.reshape(-1, 3).astype(np.float32) / 255.0

    # Scatter image pixels
    s = (4)**2  # marker size
    ax_67.scatter(
        x_flat, y_flat,
        c=colours,
        marker='s',
        s=s,
        edgecolors='none',
        zorder=2
    )

    if np.isclose(obj_x, f, atol=1e-6):
        proj_x, proj_y = np.nan, np.nan
    else:
        proj_x = -f * obj_x / (obj_x - f)
        proj_y = (obj_y / obj_x) * proj_x

    # Rays ----------------------------------------------------------------------------------------------------
    # Ray 1: horizontal from obj to lens, then refract through focal point on left
    # segment 1
    ax_67.plot([obj_x, 0], [obj_y, obj_y], color='blue')
    # segment 2
    dx1, dy1 = -f - 0, 0 - obj_y
    norm1 = np.hypot(dx1, dy1)
    x_end1 = 0 + dx1/norm1 * 10000
    y_end1 = obj_y + dy1/norm1 * 10000
    ax_67.plot([0, x_end1], [obj_y, y_end1], color='blue')

    # Ray 2: through centre of lens
    ax_67.plot([obj_x, 0], [obj_y, proj_y], color='red')
    dx2, dy2 = proj_y - obj_y, 0 - proj_y  # direction roughly horizontal
    norm2 = np.hypot(-10 - 0, 0)
    x_end2 = 0 + (-10 - 0)/np.hypot(-10,0) * 10000
    ax_67.plot([0, x_end2], [proj_y, proj_y], color='red')

    # Ray 3: to centre of ens
    dx3, dy3 = 0 - obj_x, 0 - obj_y
    norm3 = np.hypot(dx3, dy3)
    x_end3 = obj_x + dx3/norm3 * 10000
    y_end3 = obj_y + dy3/norm3 * 10000
    ax_67.plot([obj_x, x_end3], [obj_y, y_end3], color='green')

    # Dashed rays for virtual image when 0 < x < f
    if 0 < obj_x < f:
        ax_67.plot([0, proj_x], [obj_y, proj_y], '--', color='blue')
        ax_67.plot([0, proj_x], [proj_y, proj_y], '--', color='red')
        ax_67.plot([obj_x, proj_x], [obj_y, proj_y], '--', color='green')

    fig_67.canvas.draw_idle()

# Mouse event handlers
def on_press(event):
    """Start dragging if object image clicked"""
    global dragging
    if event.inaxes != ax_67 or event.button != 1:
        return
    # Check if click inside object image extent
    if (obj_x - W*0.5*0.5 <= event.xdata <= obj_x + W*0.5*0.5 and
        obj_y - H*0.5      <= event.ydata <= obj_y):
        dragging = True


def on_motion(event):
    """Update object position while dragging"""
    global obj_x, obj_y
    if not dragging or event.inaxes != ax_67:
        return
    obj_x = np.clip(event.xdata, X_MIN, X_MAX)
    obj_y = np.clip(event.ydata, Y_MIN, Y_MAX)
    redraw()


def on_release(event):
    """Stop dragging"""
    global dragging
    if event.button != 1:
        return
    dragging = False
    redraw()

# Run simulation
fig_67, ax_67 = plt.subplots()
redraw()
fig_67.canvas.mpl_connect('button_press_event', on_press)
fig_67.canvas.mpl_connect('motion_notify_event', on_motion)
fig_67.canvas.mpl_connect('button_release_event', on_release)
plt.show()