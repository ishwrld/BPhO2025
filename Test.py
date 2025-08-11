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
from PIL import Image

# Parameters from the image
Rf = 3
arc_deg = 160
sybil_pos = (0, -7)  # SYBIL position at bottom
x_pos = (0, 0)       # X position at center
scale_numbers = list(range(-7, 2)) + list(range(-6, 7))  # Scale numbers from image

# Create figure
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.axis('off')  # Hide axes

# Load SquareEinstein.jpg (replace with actual path)
try:
    einstein_img = Image.open("SquareEinstein.jpg")
    ax.imshow(einstein_img, extent=[-1, 1, -1, 1], alpha=0.5)
except:
    print("SquareEinstein.jpg not found - proceeding without it")

# Draw the arc
theta = np.linspace(-np.radians(arc_deg/2), np.radians(arc_deg/2), 100)
arc_x = Rf * np.sin(theta)
arc_y = Rf * np.cos(theta) - Rf  # Shift down by Rf to center at base
ax.plot(arc_x, arc_y, 'r-', linewidth=2)

# Add SYBIL and X markers
ax.plot(sybil_pos[0], sybil_pos[1], 'r*', markersize=15, label='Base (Red Star)')
ax.plot(x_pos[0], x_pos[1], 'kx', markersize=10, label='Center X')

# Add scale numbers
# Left vertical scale
for i, num in enumerate(range(-7, 2)):
    ax.text(-1.2, i-7, str(num), ha='center', va='center')
    
# Right vertical scale
for i, num in enumerate(range(-6, 7)):
    ax.text(1.2, i-6, str(num), ha='center', va='center')

# Add parameters text
ax.text(0, -9, f"arc_deg = {arc_deg}\nRf = {Rf}", ha='center', va='center')

# Add title
ax.set_title("Challenge #10: Unit Circle to Arc Mapping", pad=20)

# Show legend
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('recreated_image.png', dpi=300, bbox_inches='tight')
plt.show()
