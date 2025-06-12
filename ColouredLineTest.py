import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 3e8  # Speed of light in m/s
wavelengths_nm = np.linspace(405, 790, 1000)
wavelengths_um = wavelengths_nm / 1000  # Convert to micrometres

# Cauchy parameters for water
A = 1.322
B = 1.589e-2
C = 1.2e-4

# Refractive index
n = A + B / wavelengths_um**2 + C / wavelengths_um**4

# Frequencies in THz
frequencies = c / (wavelengths_nm * 1e-9) / 1e12  # in THz

# Function to map frequency to RGB
def frequency_to_rgb(f):
    if f < c / (790e-9) / 1e12:  # Lower than red
        return [np.nan, np.nan, np.nan]
    elif f < c / (680e-9) / 1e12:
        return [127/255, 0, 1]  # Violet
    elif f < c / (620e-9) / 1e12:
        return [0, 0, 1]  # Blue
    elif f < c / (600e-9) / 1e12:
        return [0, 1, 1]  # Cyan
    elif f < c / (530e-9) / 1e12:
        return [0, 1, 0]  # Green
    elif f < c / (510e-9) / 1e12:
        return [1, 1, 0]  # Yellow
    elif f < c / (480e-9) / 1e12:
        return [1, 127/255, 0]  # Orange
    elif f < c / (405e-9) / 1e12:
        return [1, 0, 0]  # Red
    else:
        return [np.nan, np.nan, np.nan]  # UV

# Generate RGB colours for each frequency
rgb_colours = np.array([frequency_to_rgb(f) for f in frequencies])

# Plot with colour mapping
fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(rgb_colours[i]).any():
        ax.plot(frequencies[i:i+2], n[i:i+2], color=rgb_colours[i], linewidth=2)

ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("Refractive Index of Water")
ax.set_title("Refractive Index vs Frequency (Coloured by Visible Spectrum)")
ax.grid(True)
plt.show()
