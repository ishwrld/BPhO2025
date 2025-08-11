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

# Import Libraries ----------------------------------------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as ctkplt


# Adding to User Interface --------------------------------------------------------------------------------------------------------------------------------------------------------
def create_task8_page(root):

    # Create Fonts
    TITLE_FONT    = ctk.CTkFont(family = 'Helvetica Nue', size = 72, weight = 'bold')
    SUBTITLE_FONT = ctk.CTkFont(family = 'Helvetica Nue', size = 32, weight = 'bold')
    TEXT_FONT     = ctk.CTkFont(family = 'Helvetica Nue', size = 24)
    TEXT_COLOUR   = '#ffffff'

    # Load Image
    obj = plt.imread("Einstein.jpg") # Put object into numpy array
    H,W = obj.shape[:2] # Get height and width (in pixels) of object image

    # Consants
    R = 500 # Radius of spherical mirror
    F = R/2

    # Bounds for the object
    X_MIN     = F
    X_MAX     = 1000
    Y_MIN     = - (R - H/2)
    Y_MAX     =   (R - H/2)

    # Initialise Variables
    obj_x = 2*F
    obj_y = 0.25 * R
    dragging = False

    # Subprograms
    def map_pixel(x_obj,y_obj):
        """
        Map an input pixel at (x_obj, y_obj) through a concave mirror of radius R,
        returning (x_img, y_img).
        """

        # Compute the square root term sqrt(R^2 - y_obj^2)
        sqrt_term = np.sqrt(R**2 - y_obj**2)
       
        # Compute theta
        theta = np.arctan2(y_obj, sqrt_term)

        # Compute m (reflected ray slope)
        m = np.tan(2 * theta)

        # Compute x_img
        x_img = -(m * sqrt_term - y_obj)/(y_obj/x_obj + m)

        # Compute y_img
        y_img = -(y_obj/x_obj) * x_img

        return x_img, y_img

    def redraw():
        """
        Clear and re‑draw the object, its warped image, and the mirror.
        """
        ax_8.clear()
        ax_8.set_xlim(-R-100, 2*R)
        ax_8.set_ylim(-1.2*R, 1.2*R)
        ax_8.set_aspect('equal')

        ax_8.set_title("Reflection in a concave mirror", color=TEXT_COLOUR)
        ax_8.set_xlabel("x", color=TEXT_COLOUR)
        ax_8.set_ylabel("y", color=TEXT_COLOUR)
        ax_8.set_facecolor('#000000')
        fig_8.patch.set_facecolor('#000000')
        ax_8.tick_params(colors=TEXT_COLOUR)
        for spine in ax_8.spines.values():
            spine.set_color(TEXT_COLOUR)
        # Draw principal axis
        ax_8.axvline(0, linestyle='--', color='gray')
        ax_8.axhline(0, linestyle='--', color='gray')


        ax_8.grid(True,        # turn the grid on
            which='both',# draw both major and minor grids
            linestyle='--',
            linewidth=0.5,
            color='gray',
            alpha=0.7)

        # Draw the concave mirror
        theta = np.linspace(np.pi/2, -np.pi/2, 200)
        x_m = (-R * np.cos(theta))
        y_m = (R * np.sin(theta))
        ax_8.plot(x_m, y_m, linewidth=2)

        # Plot mirror centre
        ax_8.plot(0, 0,
            marker='x',
            color='red',
            markersize=8,
            label='Centre of curvature')  
       
        # Plot focal point
        ax_8.plot(F, 0,
            marker='x',
            color='blue',
            markersize=8,
            label='Focal point')
           
       
        # Establish initial coordinate boundaries for object
        obj_extent = [(obj_x - W / 2), # x min
                    (obj_x + W / 2), # x max
                    (obj_y - H / 2), # y min
                    (obj_y + H / 2)] # y max

        # Display Object on graph
        ax_8.imshow(obj,
                    extent = obj_extent,
                    origin = 'upper'
                    )
       
        # Compute Warped Image Coordinates
        x_vals = np.linspace(obj_extent[0], obj_extent[1], W)
        y_vals = np.linspace(obj_extent[2], obj_extent[3], H)

        x_obj, y_obj = np.meshgrid(x_vals, y_vals)

        x_img,y_img = map_pixel(x_obj,y_obj) # Map every pixel's coordinates in object into image coordinates

        # Convert 2D Grid to 1D list (for scatter)
        x_flat = x_img.ravel()
        y_flat = y_img.ravel()

        # Remap colour of each pixel
        colours = obj.reshape(-1, 3).astype(np.float32) / 255.0

        s = (2)**2 # Size of Marker

        # Plot Image
        ax_8.scatter(
            x_flat, y_flat,
            c=colours,
            marker='s',
            s=s,
            edgecolors='none'
        )

        fig_8.canvas.draw_idle()

    def on_press(event):
        '''
        Check if left click drag is occuring on the matplotlib graph AND in the image
        '''
        nonlocal dragging

        # Check if left-click in graph
        if event.inaxes != ax_8:
            return
       
        # Check if left-click in the object
        if (obj_x - W/2 <= event.xdata <= obj_x + W/2 and obj_y - H/2 <= event.ydata <= obj_y + H/2) :
            dragging = True

    def on_motion(event):
        nonlocal obj_x, obj_y, dragging

        # Check if dragging and still in graph
        if not dragging or event.inaxes != ax_8:
            return
       
        obj_x = np.clip(event.xdata, X_MIN, X_MAX)
        obj_y = np.clip(event.ydata, Y_MIN, Y_MAX)
       
        redraw()

    def on_release(event):
        nonlocal dragging
        if not dragging:
            return
       
        dragging = False

        redraw()

    '''User Interface'''
    master = ctk.CTkFrame(root, fg_color='#000000')
    title_8 = ctk.CTkLabel(master, text = "Task 8", font = TITLE_FONT, text_color = TEXT_COLOUR)
    title_8.pack(pady = 30)

    task_8 = ctk.CTkLabel(
        master,
        text = ("Create an interactive model of the real image of an object in a concave spherical mirror"),        font = TEXT_FONT,
        text_color = TEXT_COLOUR
    )
    task_8.pack(pady = 30)

    # Run simulation
    fig_8, ax_8 = plt.subplots()
    redraw()

    graph_8 = ctkplt(fig_8, master)
    graph_8.mpl_connect('button_press_event',   on_press)
    graph_8.mpl_connect('motion_notify_event',  on_motion)
    graph_8.mpl_connect('button_release_event', on_release)
    graph_8.draw()
    graph_8.get_tk_widget().pack(expand=True, fill='both')

    return master

if __name__ == "__main__":
    ctk.set_appearance_mode('dark')
    root = ctk.CTk()
    root.geometry("1000x600")
    page = create_task8_page(root)
    page.pack(expand = True, fill = 'both')
    root.mainloop()