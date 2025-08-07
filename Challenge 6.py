import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Initialising
og_img = cv2.imread(r"Einstein.jpg")
OBJECT = cv2.cvtColor(og_img, cv2.COLOR_BGR2RGB)
H, W = OBJECT.shape[:2]
# Scale down height and width so image fits in plot
HEIGHT = H# * 0.005 # Scale factor divides by 200
WIDTH = W# * 0.005

F = 300 #Focal length
X_MIN = F + WIDTH / 2 # Bounds for image
# NOT DOING X_MAX/Y_MIN/Y_MAX FOR NOW

object_coord = (2 * F, 0) # x,y initial coordinates of image centre
object_extent = [object_coord[0] - WIDTH / 2,   # left
                object_coord[0] + WIDTH / 2,    # right
                object_coord[1] - HEIGHT / 2,   # bottom
                object_coord[1] + HEIGHT / 2]   # top
# EXTENT = [left, right, bottom, top]]
dragging = False

fig, ax = plt.subplots()
# ax.set_xlim(-6, 6)
# ax.set_ylim(-6, 6)
ax.set_xlim(-1500, 1500)
ax.set_ylim(-1500, 1500)
ax.set_aspect('equal')
ax.set_title("Image of object in a converging lens")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, linestyle='--')

# Lens and focal points
lens = Ellipse((0, 0), width=0.2*F, height=2*F, color='blue', fill=False)
ax.add_patch(lens)
ax.plot(-F, 0, marker='x', color='blue')
ax.plot(F, 0, marker='x', color='blue')

object_shown = ax.imshow(OBJECT, extent=object_extent)

def challenge_5(px,py): 
    new_x = -px #Flip image horizontally
    new_y = py    
    return new_x, new_y

def challenge_6(px,py):
    divisor = np.where(px == F, 1e-6, px - F)  # Avoid division by zero
    new_x = - F * px / divisor
    new_y = (py * new_x) / px
    return new_x, new_y

def challenge_test(px, py):
    new_x = 2 * px
    new_y = 2 * py
    return new_x, new_y

def create_virtual(pobject_extent):
    global OBJECT, ax
    left = pobject_extent[0]
    right = pobject_extent[1]
    bottom = pobject_extent[2]
    top = pobject_extent[3]
    object_width = right - left
    object_height = top - bottom

    x_coords, y_coords = np.meshgrid(np.linspace(left, right, WIDTH),
                                     np.linspace(bottom, top,HEIGHT))
    # So each coordinate is a pixel
    x_real, y_real = challenge_5(x_coords, y_coords)

    print("X blank:", x_coords)
    print("Y blank:", y_coords)
    print("X real:", x_real)
    print("Y real:", y_real)

    virtual_extent =[x_real.min(), x_real.max(), y_real.min(), y_real.max()]
    virtual_width = virtual_extent[1] - virtual_extent[0]
    virtual_height = virtual_extent[3] - virtual_extent[2]

    canvas_w = int(virtual_width / (object_width / WIDTH))
    canvas_h = int(virtual_height / (object_height / HEIGHT))

    print("Canvas size:", canvas_w, canvas_h)

    '''
    # Create meshgrid for the canvas
    x, y = np.meshgrid(np.linspace(left, right, canvas_w),
                       np.linspace(bottom, top, canvas_h))
    x_real, y_real = challenge_6(x, y)
    '''

    print("Virtual width:", virtual_width)
    print("Virtual height:", virtual_height)
    print("Object width:", object_width)
    print("Object height:", object_height)
    print("Image size:", W, H)

    width_scale = (object_width / virtual_height)# * (WIDTH)
    height_scale = (object_height / virtual_height)# * (HEIGHT)
    # width_scale = 1
    # height_scale = 1
    map_x = (x_real - virtual_extent[0]) * width_scale  #NOT SURE IF SCALING NEEDED
    map_y = (y_real - virtual_extent[2]) * height_scale #NOT SURE IF SCALING NEEDED

    print("Object extent:", pobject_extent)
    print("Virtual extent:", virtual_extent)
    print("Mapped extent:", map_x.min(), map_x.max(), map_y.min(), map_y.max())

    padded_object = cv2.copyMakeBorder(OBJECT,
                                        top=0, bottom=canvas_h - H,
                                        left=0, right=canvas_w - W,
                                        borderType=cv2.BORDER_CONSTANT,
                                        value=(30, 60, 190))  # Green background
    
    blank_x = np.full((canvas_h, canvas_w),-1, dtype=np.float32)  # Blank mapping to put x_real onto
    blank_y = np.full((canvas_h, canvas_w),-1, dtype=np.float32)  # Blank mapping to put y_real onto

    print("Shape of blank_x:", blank_x.shape)
    print("Shape of blank_y:", blank_y.shape)
    print("Shape of map_x:", map_x.shape)
    print("Shape of map_y:", map_y.shape)

    blank_x[0:H, 0:W] = map_x
    blank_y[0:H, 0:W] = map_y
    
    img = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
    img = cv2.remap(
        padded_object, blank_x.astype(np.float32), blank_y.astype(np.float32),
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 0, 0)  # RED in RGB
        )
    cv2.imshow("Original Image", OBJECT)
    cv2.imshow("Padded Image", padded_object)
    cv2.imshow("Remapped Image", img)
    

    '''
    Things to fix:
    - Fix x_real, y_real as remap starts from top left corner
    - Make object image on larger canvas by adding white space to the right and bottom
    - x_real, y_real need to account for white space by having all whitespace coords to -1
    - check map_x, map_y are correct
    '''

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
            try:
                virtual_shown.remove()
            except Exception as e:
                print("No virtual image to remove:", e)
            virtual_shown = create_virtual(obj_extent)

    fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()
    
