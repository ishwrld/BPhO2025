import matplotlib.pyplot as plt
import numpy as np  

def findIndexWater(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

# def primaryReflectance(angle, n):
#     return 180 - 6 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) + 2 * angle

# def secondaryReflectance(angle, n):
#     return 4 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) - 2 * angle

# def primaryMinimum(n):
#     return primaryReflectance(np.rad2deg(np.arcsin(((9 - n ** 2) / 8) ** 0.5)),n)

# def secondaryMinimum(n):
#     return secondaryReflectance(np.rad2deg(np.arcsin(((4 - n ** 2) / 3) ** 0.5)), n)

def primaryMinimum(n):
    angle = np.arcsin(((9 - n ** 2) / 8) ** 0.5)
    rad = np.pi - 6 * np.arcsin(np.sin(angle) / n) + 2 * angle
    return np.rad2deg(rad)

def secondaryMinimum(n):
    angle = np.arcsin(((4 - n ** 2) / 3) ** 0.5)
    rad = 4 * np.arcsin(np.sin(angle) / n) - 2 * angle
    return np.rad2deg(rad)

def chooseColour(freq):
    if freq < 405:  # Lower than red
        return [np.nan, np.nan, np.nan]
    if freq < 480:
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

frequencies = np.linspace(400, 750, 350)
indexes = findIndexWater(frequencies)
primary = primaryMinimum(indexes)
secondary = secondaryMinimum(indexes)
colour = np.array([chooseColour(f) for f in frequencies])

fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(colour[i]).any():
        ax.plot(frequencies[i:i+2], primary[i:i+2], color=colour[i], linewidth=2, label='Primary' if i == 0 else "")
        ax.plot(frequencies[i:i+2], secondary[i:i+2], color=colour[i], linestyle='--', linewidth=2, label='Secondary' if i == 0 else "")

ax.set_xlim(frequencies.min(), frequencies.max())
ax.set_ylim(min(primary.min(), secondary.min())-0.5, max(primary.max(), secondary.max())+0.5)
ax.set_title("Elevation of single and double rainbows")
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("ε (degrees)")
ax.annotate("Primary Rainbow", (415,42.35))
ax.annotate("Secondary Rainbow", (600, 50.15))

ax.grid(True, dashes = [1,1], alpha = 0.25)

plt.show()
