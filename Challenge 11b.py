import matplotlib.pyplot as plt
import numpy as np  

def formula(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

def primaryReflectance(angle, n):
    return 180 - 6 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) + 2 * angle

def secondaryReflectance(angle, n):
    return 4 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) - 2 * angle

def primaryMinimum(n):
    return primaryReflectance(np.rad2deg(np.arcsin(((9 - n ** 2) / 8) ** 0.5)),n)

def secondaryMinimum(n):
    return secondaryReflectance(np.rad2deg(np.arcsin(((4 - n ** 2) / 3) ** 0.5)), n)

def chooseColour(freq):
    if freq < 405:  # Lower than red
        return [np.nan, np.nan, np.nan]
    elif freq < 480:
        return [(freq-405)/75,0,0]  # Red
    elif freq < 510:
        return [1, ((freq-480)/30)*127/255, 0]  # Orange
    elif freq < 530:
        return [1, 127/255 + ((freq-510)/20)*128/255, 0]  # Yellow
    elif freq < 600:
        return [1-(freq-530)/70, 1, 0]  # Green
    elif freq < 620:
        return [0, 1, (freq-600)/20]  # Cyan    
    elif freq < 680:
        return [0, 1-(freq-620)/60, 1]  # Blue
    elif freq < 790:
        return [((freq-680)/110)*127/255, 0, 1]  # Violet
    else:
        return [np.nan, np.nan, np.nan]  

frequencies = np.linspace(450, 750, 300)
primary = primaryMinimum(formula(frequencies))
secondary = secondaryMinimum(formula(frequencies))
colour = np.array([chooseColour(f) for f in frequencies])

fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(colour[i]).any():
        ax.plot(frequencies[i:i+2], primary[i:i+2], color=colour[i], linewidth=2, label='Primary' if i == 0 else "")
        ax.plot(frequencies[i:i+2], secondary[i:i+2], color=colour[i], linestyle='--', linewidth=2, label='Secondary' if i == 0 else "")

ax.set_xlim(frequencies.min(), frequencies.max())
ax.set_ylim(min(primary.min(), secondary.min())-1, max(primary.max(), secondary.max())+1)
ax.set_title("Elevation of single and double rainbows")
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("Elevation (degrees)")

plt.grid(True)
plt.show()
