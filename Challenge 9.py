import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# CONSTANTS
OBJECT = plt.imread("Einstein.jpg")
HEIGHT, WIDTH = OBJECT.shape[:2]
SCALE = 0.5 # Scale down image to look better
SCALE_H = HEIGHT * SCALE
SCALE_W = WIDTH * SCALE
R = 600 * SCALE # Radius
X_MIN = R + SCALE_W / 2
X_MAX = 2 * R - SCALE_W / 2
COLOURS = OBJECT.reshape(-1, 3).astype(np.float32) / 255.0

# FUNCTIONS
def challenge_9(px,py):
    alpha = 0.5 * np.arctan(py/px)
    k = px / np.cos(2 * alpha)
    new_y = k * np.sin(alpha) / (k / R - np.cos(alpha) + px * np.sin(alpha) / py)
    new_x = px * new_y / py
    return new_x, new_y

#print(challenge_9(598,638))

def create_virtual(pobject_extent, scatter_image = None):
    '''Create a virtual image based on the object extent'''
    global OBJECT, WIDTH, HEIGHT, COLOURS, ax
    # Create meshgrid for object coordinates
    object_x, object_y = np.meshgrid(
        np.linspace(pobject_extent[0], pobject_extent[1], WIDTH),
        np.linspace(pobject_extent[3], pobject_extent[2], HEIGHT)
    )

    # Map object coordinates to image coordinates
    image_x, image_y = challenge_9(object_x, object_y)
    map_x = image_x.ravel() # Flatten into 1D array
    map_y = image_y.ravel() # Flatten into 1D array
    
    # Remove old image
    if scatter_image != None:
        scatter_image.remove()
    
    # Create scatter plot for virtual image
    scatter_image = ax.scatter(
        map_x, map_y,
        c = COLOURS,
        marker = ',', 
        s = 1,  # Size of each point
        edgecolors = "none",
        zorder = 1
    )

    return scatter_image

def draw_rays(x_coord, y_coord, rays = []):
    global R, ax
    x_img, y_img = challenge_9(x_coord, y_coord) # Image coordinates

    # Clear any old rays
    if rays != []:
        for ray in rays:
            ray.remove()
    
    c_x = -(R ** 2 - y_coord ** 2) ** 0.5 # X coordinate of point on circle
    point_c, = ax.plot(c_x, y_coord)
    main_ray, = ax.plot([x_coord, c_x, x_img, x_coord], [y_coord, y_coord, y_img, y_coord], 
                        linestyle = '-', linewidth = 0.5, color = 'red', zorder = 5)
    second_ray, = ax.plot([c_x, 0], [y_coord, 0], 
                        linestyle = '--', linewidth = 0.5, color = 'blue', zorder = 5)

    rays = [point_c, main_ray, second_ray]
        
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
    global dragging, virtual_shown, object_shown, rays1, rays2
    if dragging and event.inaxes == ax:
        coord = (event.xdata, event.ydata) # Mouse coordinates taken as centre of image
        if X_MIN < coord[0] < X_MAX:    # To reduce lag when virtual gets too big
            obj_extent = [coord[0] - SCALE_W / 2,       # left
                            coord[0] + SCALE_W / 2,     # right
                            coord[1] - SCALE_H / 2,     # bottom
                            coord[1] + SCALE_H / 2]     # top
            object_shown.set_extent(obj_extent)
            virtual_shown = create_virtual(obj_extent, virtual_shown)
            #rays1 = draw_rays(coord[0], obj_extent[3], rays1)
            #rays2 = draw_rays(obj_extent[0], obj_extent[3], rays2)

    fig.canvas.draw_idle()

# Initialising plot
dragging = False
fig, ax = plt.subplots()
ax.set_xlim(-0.1 * R, R * 2)
ax.set_ylim(-R * 1.2, R * 1.2)
ax.set_aspect('equal')
ax.set_title("Reflection in a convex mirror")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle = '--')

# Mirror and its centre and focal point
mirror = Arc((0, 0), width = 2 * R, height = 2 * R, angle = 180, 
             theta1 = 90, theta2 = -90, color = 'blue', zorder = 3)
ax.add_patch(mirror)
ax.plot(0, 0, marker = 'x', color = 'blue', zorder = 7)

# Initial object coordinates and extent
object_coord = (1.25 * R, SCALE_W) # Initial object coordinates
object_extent = [object_coord[0] - SCALE_W / 2,    # left
                object_coord[0] + SCALE_W / 2,     # right
                object_coord[1] - SCALE_H / 2,     # bottom
                object_coord[1] + SCALE_H / 2]     # top

# Show object and virtual images and rays
object_shown = ax.imshow(OBJECT, extent = object_extent, zorder = 2)
virtual_shown = create_virtual(object_extent)
rays1 = draw_rays(object_coord[0], object_extent[3])
rays2 = draw_rays(object_extent[0], object_extent[3])

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()