import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Initialising
OBJECT = cv2.cvtColor(cv2.imread(r"Einstein.jpg"), cv2.COLOR_BGR2RGB)
H, W = OBJECT.shape[:2]
# Scale down height and width so image fits in plot
HEIGHT = H * 0.005 # Scale factor divides by 200
WIDTH = W * 0.005

F = 1.5 #Focal length
X_MIN = F / 2 + WIDTH / 2 # Bounds for image
# NOT DOING X_MIN/Y_MIN/Y_MAX FOR NOW

object_coord = (2 * F, 0) # x,y initial coordinates of image centre
object_extent = [object_coord[0] - WIDTH / 2,   # left
                object_coord[0] + WIDTH / 2,    # right
                object_coord[1] - HEIGHT / 2,   # bottom
                object_coord[1] + HEIGHT / 2]   # top
# EXTENT = [left, right, bottom, top]]
dragging = False

fig, ax = plt.subplots()
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')
ax.set_title("Image of object in a converging lens")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle='--')

# Lens and focal points
lens = Ellipse((0, 0), width=0.2, height=2*F, color='blue', fill=False)
ax.add_patch(lens)
ax.plot(-F, 0, marker='x', color='blue')
ax.plot(F, 0, marker='x', color='blue')

object_shown = ax.imshow(OBJECT, extent=object_extent)

def challenge_5(px,py): 
    new_x = -px #Flip image horizontally
    new_y = py    
    # Ensure maps are float32 for remap()
    return new_x.astype(np.float32), new_y.astype(np.float32)


def challenge_6(px,py):
    divisor = np.where(px == F, 1e-6, px - F)  # Avoid division by zero
    new_x = - F * px / divisor
    new_y = py * new_x / px
    return new_x.astype(np.float32), new_y.astype(np.float32)

def create_virtual(pobject_extent):
    global OBJECT, ax
    left = pobject_extent[0]
    right = pobject_extent[1]
    bottom = pobject_extent[2]
    top = pobject_extent[3]

    x_coords, y_coords = np.meshgrid(np.linspace(left, right, W),
                                     np.linspace(bottom, top,H))
    # So each coordinate is a pixel
    x_real, y_real = challenge_6(x_coords, y_coords)

    virtual_extent =[x_real.min(), x_real.max(), y_real.min(), y_real.max()]
    virtual_width = virtual_extent[1] - virtual_extent[0]
    virtual_height = virtual_extent[3] - virtual_extent[2]
    #print("Width:", virtual_width)
    #print("Height:", virtual_height)
    #print(W, H)
    map_x = (x_real - virtual_extent[0]) * (virtual_width) * (W - 1)
    map_y = (y_real - virtual_extent[2]) * (virtual_height) * (H - 1)

    img = cv2.remap(
        OBJECT, map_x.astype(np.float32), map_y.astype(np.float32),
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 0, 0)  # RED in RGB
        )
    cv2.imshow("Remapped Image", img)

    return ax.imshow(img, extent=virtual_extent)

virtual_shown = create_virtual(object_extent)

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
    global dragging, virtual, virtual_shown
    if dragging and event.inaxes == ax:
        coord = (event.xdata, event.ydata)
        if coord[0] > X_MIN:
            obj_extent = [coord[0] - WIDTH / 2,  # left
                            coord[0] + WIDTH / 2,   # right
                            coord[1] - HEIGHT / 2,  # bottom
                            coord[1] + HEIGHT / 2]  # top
            object_shown.set_extent(obj_extent)
            virtual_shown.remove()
            virtual_shown = create_virtual(obj_extent)

    fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()
    
