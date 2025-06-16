import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

fig, ax = plt.subplots()
ax.set_ylim(-6,6)
ax.set_xlim(-6,6)
ax.grid(True, linestyle=':')
plt.title("Image in a Converging Lense")

image_path = r"Einstein.jpg"
img = Image.open(image_path)
img_array = np.array(img)
imgT_array = np.array(img)

imgT_extent = []

ax.imshow(img_array, extent=[2,4,0,2], zorder=1)





plt.show()