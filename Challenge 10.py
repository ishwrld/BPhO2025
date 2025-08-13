import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

# CONSTANTS
OBJECT = plt.imread("SquareEinstein.jpg")
HEIGHT, WIDTH = OBJECT.shape[:2]
RADIUS = 1 # Radius of circle (in this case unit circle)
SCALE = RADIUS * 2 ** 0.5 / HEIGHT # Scale down image to make it 1 by 1
SCALE_H = HEIGHT * SCALE
SCALE_W = WIDTH * SCALE
COLOURS = OBJECT.reshape(-1, 3).astype(np.float32) / 255.0
RF = 3 # Radius of circle arc
ARC_DEG = 160
ARC_RAD = np.deg2rad(ARC_DEG)
IMG_LENGTH = SCALE_H * RF
AXIS_LIMS = [(-2 * RADIUS * RF, 2 * RADIUS * RF),       # (x min, x max) 
             (-int(IMG_LENGTH + 2 + RADIUS), 2*RADIUS)] # (y min, y max)

# FUNCTIONS
def challenge_10(px, py):
    norm_x = px
    norm_y = py + SCALE_H / 2

    angle = ARC_RAD * norm_x / SCALE_W
    r = RADIUS + IMG_LENGTH * norm_y / SCALE_H

    new_x = r * np.sin(angle)
    new_y = - r * np.cos(angle) - SCALE_H / 2

    return new_x, new_y

def create_virtual(pobject_extent):
    '''Create a virtual image based on the object extent'''
    global OBJECT, WIDTH, HEIGHT, COLOURS, ax
    # Create meshgrid for object coordinates
    object_x, object_y = np.meshgrid(
        np.linspace(pobject_extent[0], pobject_extent[1], WIDTH),
        np.linspace(pobject_extent[3], pobject_extent[2], HEIGHT)
    )

    # Map object coordinates to image coordinates
    image_x, image_y = challenge_10(object_x, object_y)
    map_x = image_x.ravel() # Flatten into 1D array
    map_y = image_y.ravel() # Flatten into 1D array

    # Create scatter plot for virtual image
    scatter_image = ax.scatter(
        map_x, map_y,
        c = COLOURS,
        marker = ',', 
        s = 5,  # Size of each point
        edgecolors = "none",
        zorder = 1
    )

    return scatter_image

# Initialising plot
fig, ax = plt.subplots()
ax.set_xlim(AXIS_LIMS[0])
ax.set_ylim(AXIS_LIMS[1])
ax.set_xticks(np.arange(AXIS_LIMS[0][0], AXIS_LIMS[0][1]+1)) 
ax.set_yticks(np.arange(AXIS_LIMS[1][0], AXIS_LIMS[1][1]+1))
ax.set_aspect('equal')
ax.set_title("An anamorphic image")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle = '-')

# Lens and focal points
circle = Circle((0, 0), RADIUS, color = 'black', fill = False, zorder = 3)
ax.add_patch(circle)
ax.plot(0, -SCALE_H/2, marker = 'x', color = 'red', zorder = 7)
arrow = dict(arrowstyle="->", color='blue', lw=1)
ax.annotate("", (AXIS_LIMS[0][1], 0), (-0.05, 0), arrowprops = arrow, zorder = 7) # X axis
ax.annotate("", (0, AXIS_LIMS[1][1]), (0, -0.05), arrowprops = arrow, zorder = 7) # Y axis

# Object coordinates and extent
object_coord = (0, 0) # Centre of object
object_extent = [object_coord[0] - SCALE_W / 2,    # left
                object_coord[0] + SCALE_W / 2,     # right
                object_coord[1] - SCALE_H / 2,     # bottom
                object_coord[1] + SCALE_H / 2]     # top

# Show object and virtual images and rays
object_shown = ax.imshow(OBJECT, extent = object_extent, zorder = 5)
virtual_shown = create_virtual(object_extent)
manager = plt.get_current_fig_manager()
manager.toolbar.pack_forget()  # Removes toolbar from Tkinter window
plt.show()