def challenge_6():
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt

    # Load image
    img = cv2.imread("Einstein.jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    # Define new canvas size (larger than original image)
    canvas_h = int(h * 1.5)
    canvas_w = int(w * 1.5)

    # Create meshgrid for the canvas
    x, y = np.meshgrid(np.arange(canvas_w), np.arange(canvas_h))

    # Shift the image right and up (into the expanded area)
    shift_x = -w // 4   # Shift left by 1/4 image width (=> into right side of canvas)
    shift_y = -h // 4   # Shift up by 1/4 image height (=> into bottom side of canvas)

    # Compute corresponding coordinates in the original image
    map_x = (x + shift_x).astype(np.float32)
    map_y = (y + shift_y).astype(np.float32)

    # Remap
    remapped = cv2.remap(
        img_rgb, map_x, map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  # white background for out-of-bounds
    )

    # Show result
    plt.figure(figsize=(8, 8))
    plt.imshow(remapped)
    plt.title("Image shifted onto larger canvas")
    plt.axis("off")
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# CONSTANTS
OBJECT = plt.imread("Einstein.jpg")
HEIGHT, WIDTH = OBJECT.shape[:2]
SCALE = 0.4 # Scale down image to look better
SCALE_H = HEIGHT * SCALE
SCALE_W = WIDTH * SCALE
F = 250 # Focal length
X_MIN = F / 2 + SCALE_W / 2 # Stop image getting too close to lens
COLOURS = OBJECT.reshape(-1, 3).astype(np.float32) / 255.0
SIZE = 1000 # Limits of axis go from -SIZE to SIZE

# FUNCTIONS
def challenge_6(px,py):
    divisor = np.where(px == F, 1e-6, px - F)  # Avoid division by zero
    new_x = - F * px / divisor
    new_y = (py * new_x) / px
    return new_x, new_y

def create_virtual(pobject_extent, scatter_image = None):
    '''Create a virtual image based on the object extent'''
    global OBJECT, WIDTH, HEIGHT, COLOURS, ax
    # Create meshgrid for object coordinates
    object_x, object_y = np.meshgrid(
        np.linspace(pobject_extent[0], pobject_extent[1], WIDTH),
        np.linspace(pobject_extent[3], pobject_extent[2], HEIGHT)
    )

    # Map object coordinates to image coordinates
    image_x, image_y = challenge_6(object_x, object_y)
    map_x = image_x.ravel() # Flatten into 1D array
    map_y = image_y.ravel() # Flatten into 1D array
    
    # Remove old image
    if scatter_image != None:
        scatter_image.remove()
    
    marker_size = 1
    if pobject_extent[0] < F:
        marker_size = 6

    # Create scatter plot for virtual image
    scatter_image = ax.scatter(
        map_x, map_y,
        c = COLOURS,
        marker = ',', 
        s = marker_size,  # Size of each point
        edgecolors = "none",
        zorder = 1
    )

    return scatter_image

def draw_rays(x_coord, y_coord, rays = []):
    global F, SIZE
    x_img, y_img = challenge_6(x_coord, y_coord) # Image coordinates

    # Clear any old rays
    if rays != []:
        for ray in rays:
            ray.remove()

    # 2 lines if real / 4 lines if virtual
    if x_coord < F: # Virtual image
        top_real, = ax.plot([x_coord, 0, -SIZE], [y_coord, y_coord, -SIZE * y_coord / F + y_coord], 
                            linestyle = '-', linewidth = 0.5, color = 'red', zorder = 5)
        middle_real, = ax.plot([x_coord, -SIZE], [y_coord, -SIZE * y_coord / x_coord], 
                            linestyle = '-', linewidth = 0.5, color = 'red', zorder = 5)
        top_virtual, = ax.plot([0, x_img], [y_coord, y_img], 
                            linestyle = '--', linewidth = 0.5, color = 'red', zorder = 5)
        middle_virtual, = ax.plot([x_coord, x_img], [y_coord, y_img], 
                            linestyle = '--', linewidth = 0.5, color = 'red', zorder = 5)
        rays = [top_real, top_virtual, middle_real, middle_virtual]
    else:
        top_real, = ax.plot([x_coord, 0, x_img], [y_coord, y_coord, y_img], 
                            linestyle = '-', linewidth = 0.5, color = 'red', zorder = 5)
        middle_real, = ax.plot([x_coord, x_img], [y_coord, y_img], 
                            linestyle = '-', linewidth = 0.5, color = 'red', zorder = 5)
        rays = [top_real, middle_real]
        
    return rays

# Moving image with mouse
def on_press(event):
    global dragging
    if event.inaxes == ax:
        contains, _ = object_shown.contains(event)
        if contains:
            dragging = True

def on_release(event):
    global dragging
    dragging = False

def on_motion(event):
    global dragging, virtual_shown, object_shown, rays
    if dragging and event.inaxes == ax:
        coord = (event.xdata, event.ydata) # Mouse coordinates taken as centre of image
        if coord[0] > X_MIN:    # To reduce lag when virtual gets too big
            obj_extent = [coord[0] - SCALE_W / 2,       # left
                            coord[0] + SCALE_W / 2,     # right
                            coord[1] - SCALE_H / 2,     # bottom
                            coord[1] + SCALE_H / 2]     # top
            object_shown.set_extent(obj_extent)
            virtual_shown = create_virtual(obj_extent, virtual_shown)
            rays = draw_rays(coord[0], obj_extent[3], rays)

    fig.canvas.draw_idle()

# Initialising plot
dragging = False
fig, ax = plt.subplots()
ax.set_xlim(-SIZE, SIZE)
ax.set_ylim(-SIZE, SIZE)
ax.set_aspect('equal')
ax.set_title("Image of object in a converging lens")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle = '--')

# Lens and focal points
lens = Ellipse((0, 0), width = 0.2 * F, height = 2 * F, color = 'blue', fill = False, zorder = 3)
ax.add_patch(lens)
ax.plot(-F, 0, marker = 'x', color = 'blue')
ax.plot(F, 0, marker = 'x', color = 'blue')

# Initial object coordinates and extent
object_coord = (2 * F, F) # Initial object coordinates
object_extent = [object_coord[0] - SCALE_W / 2,    # left
                object_coord[0] + SCALE_W / 2,     # right
                object_coord[1] - SCALE_H / 2,     # bottom
                object_coord[1] + SCALE_H / 2]     # top

# Show object and virtual images and rays
object_shown = ax.imshow(OBJECT, extent = object_extent, zorder = 2)
virtual_shown = create_virtual(object_extent)
rays = draw_rays(object_coord[0], object_extent[3])

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()