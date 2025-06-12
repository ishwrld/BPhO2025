import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

fig, ax = plt.subplots()

ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.axvline(x=0, color='purple', linestyle='--', linewidth=1.5)
plt.title("Reflection in a Plane Mirror")

image_path = r"C:\Users\msesh\OneDrive\Documents\BPhO\Screenshot.png"
img = Image.open(image_path)
img_array = np.array(img)
virtual_img_array = np.fliplr(img_array)

ax.imshow(img_array, extent=[1, 5, -2, 2], zorder=1)
ax.imshow(virtual_img_array, extent=[-5, -1, -2, 2], zorder=1)
ax.text(2.05, 3, "object", color='red', fontsize=12)
ax.text(-4, 3, "virtual image", color='green', fontsize=12)
ax.grid(True, linestyle= ':')


plt.show()
