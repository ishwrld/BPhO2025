import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from skimage import transform
from skimage.io import imread
from skimage.transform import ProjectiveTransform, warp, rotate

# Load the image
sign = imread('Einstein.jpg')  # raw string not needed unless using special chars

# Show rotated image
plt.figure(figsize=(8, 6), dpi=80)
sign_rotate = rotate(sign, 330, preserve_range=True)
plt.imshow(sign_rotate.astype(np.uint8))  # Ensure image is uint8 for display
plt.axis('off')
plt.show()

# Function to compare different fill modes during rotation
def rotate_fills(image):
    modes = ['constant', 'edge', 'symmetric', 'reflect', 'wrap']
    fig, ax = plt.subplots(3, 2, figsize=(7, 10), dpi=200)
    for n, a in enumerate(ax.flatten()):
        if n == 0:
            a.set_title('original', fontsize=12)
            a.imshow(image)
        else:
            a.set_title(modes[n-1], fontsize=12)
            rotated = rotate(image, 330, mode=modes[n-1], preserve_range=True)
            a.imshow(rotated.astype(np.uint8))
        a.axis('off')
    fig.tight_layout()
    plt.show()

rotate_fills(sign)

# Function to compare 'symmetric' and 'reflect'
def comparing_fills(image):
    modes = ['symmetric', 'reflect']
    fig, ax = plt.subplots(1, 2, figsize=(7, 10), dpi=200)
    for i in range(2):
        rotated = rotate(image, 330, mode=modes[i], preserve_range=True)
        ax[i].imshow(rotated.astype(np.uint8))
        ax[i].set_title(modes[i], fontsize=15)
        ax[i].axis('off')
    fig.tight_layout()
    plt.show()

comparing_fills(sign)

# Points for projection transform
points_of_interest = np.array([[360, 110], 
                               [420, 270], 
                               [130, 400], 
                               [100, 280]])
projection = np.array([[500, 200],
                       [500, 390],
                       [100, 390],
                       [100, 200]])

# Draw original and projected points
color = 'red'
fig, ax = plt.subplots(1, 2, figsize=(15, 10), dpi=80)
for pt in points_of_interest:
    ax[0].add_patch(Circle(tuple(pt), 10, facecolor=color))
ax[0].imshow(sign)
ax[0].axis('off')

for pt in projection:
    ax[1].add_patch(Circle(tuple(pt), 10, facecolor=color))
ax[1].imshow(np.ones_like(sign))  # blank canvas
ax[1].axis('off')
plt.show()

# Apply projective transformation
tform = ProjectiveTransform()
tform.estimate(points_of_interest, projection)

tf_img_warp = warp(sign, tform.inverse, mode='symmetric', preserve_range=True)

# Show transformation result
fig, ax = plt.subplots(1, 2, figsize=(15, 10), dpi=80)
ax[0].set_title('Original', fontsize=15)
ax[0].imshow(sign)
ax[0].axis('off')

ax[1].set_title('Transformed', fontsize=15)
ax[1].imshow(tf_img_warp.astype(np.uint8))
ax[1].axis('off')
plt.show()
