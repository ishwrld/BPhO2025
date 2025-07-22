# import os 
# import cv2 as cv
# import numpy as np
# import matplotlib.pyplot as plt

# f = 0.5
# import matplotlib.transforms as mtransforms

# fig, ax = plt.subplots()

# img = cv.imread(r'Einstein.jpg')

# height, width = img.shape

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load image
img = Image.open("Einstein.jpg").convert("L")  # grayscale
img_array = np.array(img)

height, width = img_array.shape

# Lens parameters
f = 100  # focal length in pixels

# Object coordinates (x, y)
y_coords, x_coords = np.indices(img_array.shape)

# Mask only where x > f (real image case)
mask = x_coords > f
x_obj = x_coords[mask]
y_obj = y_coords[mask]

# Lens formula: v = (u*f)/(u - f)
u = x_obj
v = (u * f) / (u - f)

# Magnification: M = -v/u
M = -v / u

# Transformed coordinates
X_img = v
Y_img = M * (y_obj - height // 2) + height // 2  # scale vertically around center

# Create empty canvas for image projection
sim_img = np.zeros_like(img_array)

# Only plot if coordinates are valid
X_img = X_img.astype(int)
Y_img = Y_img.astype(int)

valid = (X_img >= 0) & (X_img < width) & (Y_img >= 0) & (Y_img < height)

sim_img[Y_img[valid], X_img[valid]] = img_array[y_obj[valid], x_obj[valid]]

# Plot original and transformed images
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(img_array, cmap='gray')
axes[0].set_title("Original (Object)")
axes[1].imshow(sim_img, cmap='gray')
axes[1].set_title("Transformed (Real Image through Convex Lens)")

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()
