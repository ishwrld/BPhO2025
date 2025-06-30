# # import numpy as np
# # import matplotlib.pyplot as plt

# # # Constants
# # c = 3e8  # Speed of light in m/s
# # wavelengths_nm = np.linspace(405, 790, 1000)
# # wavelengths_um = wavelengths_nm / 1000  # Convert to micrometres

# # # Cauchy parameters for water
# # A = 1.322
# # B = 1.589e-2
# # C = 1.2e-4

# # # Refractive index
# # n = A + B / wavelengths_um**2 + C / wavelengths_um**4

# # # Frequencies in THz
# # frequencies = c / (wavelengths_nm * 1e-9) / 1e12  # in THz

# # # Function to map frequency to RGB
# # def frequency_to_rgb(f):
# #     if f < c / (790e-9) / 1e12:  # Lower than red
# #         return [np.nan, np.nan, np.nan]
# #     elif f < c / (680e-9) / 1e12:
# #         return [127/255, 0, 1]  # Violet
# #     elif f < c / (620e-9) / 1e12:
# #         return [0, 0, 1]  # Blue
# #     elif f < c / (600e-9) / 1e12:
# #         return [0, 1, 1]  # Cyan
# #     elif f < c / (530e-9) / 1e12:
# #         return [0, 1, 0]  # Green
# #     elif f < c / (510e-9) / 1e12:
# #         return [1, 1, 0]  # Yellow
# #     elif f < c / (480e-9) / 1e12:
# #         return [1, 127/255, 0]  # Orange
# #     elif f < c / (405e-9) / 1e12:
# #         return [1, 0, 0]  # Red
# #     else:
# #         return [np.nan, np.nan, np.nan]  # UV

# # # Generate RGB colours for each frequency
# # rgb_colours = np.array([frequency_to_rgb(f) for f in frequencies])

# # # Plot with colour mapping
# # fig, ax = plt.subplots()
# # for i in range(len(frequencies) - 1):
# #     if not np.isnan(rgb_colours[i]).any():
# #         ax.plot(frequencies[i:i+2], n[i:i+2], color=rgb_colours[i], linewidth=2)

# # ax.set_xlabel("Frequency (THz)")
# # ax.set_ylabel("Refractive Index of Water")
# # ax.set_title("Refractive Index vs Frequency (Coloured by Visible Spectrum)")
# # ax.grid(True)
# # plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image

# fig, ax = plt.subplots()

# ax.set_xlim(-6, 6)
# ax.set_ylim(-6, 6)
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')

# image_path = r"Einstein.jpg"
# image = Image.open(image_path)
# img_array = np.array(image)
# virtual_img_array = np.fliplr(img_array)

# virtual_ex = [-5, -1, -2, 2]
# real_ex = [1, 5, -2, 2]

# Virtual_image = ax.imshow(virtual_img_array, extent=virtual_ex, zorder=1)
# real_image = ax.imshow(img_array, extent=real_ex, zorder=1)

# print(img_array)
# #print(virtual_img_array)

# plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Ellipse
from scipy.ndimage import map_coordinates

# === Settings ===

f = 0.5    # focal length of lens
x_obj = 1.0  # x-position of object
scale = 0.5  # size scale for images

# === Load object image ===

img = mpimg.imread(r'Einstein.jpg')
H, W = img.shape[0], img.shape[1]

# === Physical coordinates for image ===

x_phys = np.linspace(-scale, scale, W)
y_phys = np.linspace(-scale, scale * H / W, H)

x_grid, y_grid = np.meshgrid(x_phys, y_phys)

# === Lens equation ===

X_new = -f * x_grid / (x_grid - f)
Y_new = (y_grid * X_new) / x_grid

# === Map back to pixel coordinates ===

X_idx = np.interp(X_new, x_phys, np.arange(W))
Y_idx = np.interp(Y_new, y_phys, np.arange(H))

X_idx_clipped = np.clip(X_idx, 0, W - 1)
Y_idx_clipped = np.clip(Y_idx, 0, H - 1)

coords = np.vstack([Y_idx_clipped.ravel(), X_idx_clipped.ravel()])

img_out = np.zeros_like(img)
for c in range(img.shape[2]):
    img_out[..., c] = map_coordinates(img[..., c], coords, order=1, mode='reflect').reshape(H, W)

# === Plot ===

fig, ax = plt.subplots(figsize=(8, 6))

# Original image at (x_obj, 0)
ax.imshow(img, extent=[x_obj - scale, x_obj + scale, -scale, scale], zorder=1)
ax.text(x_obj, scale + 0.1, r'$(x, y)$', ha='center', fontsize=12)

# Virtual image at X_obj
X_obj = -f * x_obj / (x_obj - f)
ax.imshow(img_out, extent=[X_obj - scale, X_obj + scale, -scale, scale], zorder=1)
ax.text(X_obj, -scale - 0.1, r'$(X, Y)$', ha='center', fontsize=12)

# Lens (ellipse)
lens = Ellipse((0, 0), width=0.2, height=3.0, edgecolor='blue', facecolor='none', lw=2)
ax.add_patch(lens)

# Focal points
ax.plot([f, -f], [0, 0], 'b*', markersize=12)

# Rays
# 1st ray → straight through center
ax.plot([x_obj, 0, X_obj], [0, 0, 0], 'r-', lw=1)
# 2nd ray → through top of object
ax.plot([x_obj, 0, X_obj], [scale, scale * 0.5, -scale], 'r-', lw=1)

# Labels and grid
ax.set_xlim(-3, 3)
ax.set_ylim(-2, 2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)
ax.set_title('Image of object in a converging lens')

plt.show()
