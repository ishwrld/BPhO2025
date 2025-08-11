import matplotlib.pyplot as plt
import numpy as np  

def formula(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

def getPhi(angle, n):
    return np.rad2deg(np.arcsin(np.sin(angle)/n))

def critAngle(n):
    return np.rad2deg(np.arcsin(1/n))

def primaryMinimum(n):
    return np.rad2deg(np.arcsin(((9 - n ** 2) / 8) ** 0.5 / n))
    #return getPhi((np.arcsin(((9 - n ** 2) / 8) ** 0.5)),n)

def secondaryMinimum(n):
    return np.rad2deg(np.arcsin(((4 - n ** 2) / 3) ** 0.5/n))
    #return getPhi((np.arcsin(((4 - n ** 2) / 3) ** 0.5)), n)

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

frequencies = np.linspace(400, 750, 350)
indexes = formula(frequencies)
critical = critAngle(indexes)
primary = primaryMinimum(indexes)
secondary = secondaryMinimum(indexes)
colour = np.array([chooseColour(f) for f in frequencies])

fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(colour[i]).any():
        ax.plot(frequencies[i:i+2], critical[i:i+2], color=[0,0,0], linewidth=1.5, label='Critical' if i == 0 else "")
        ax.plot(frequencies[i:i+2], primary[i:i+2], color=colour[i], linewidth=1.5, label='Primary' if i == 0 else "")
        ax.plot(frequencies[i:i+2], secondary[i:i+2], color=colour[i], linewidth=1.5, label='Secondary' if i == 0 else "")

ax.set_xlim(frequencies.min(), frequencies.max())
ax.set_ylim(secondary.min()-0.05, critical.max()+0.05)
ax.set_title("Refraction angle of single and double rainbows")
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("ϕ (degrees)")
ax.annotate("Critical angle", (415,48.5))
ax.annotate("Primary", (415,45.4))
ax.annotate("Secondary", (415, 40.7))
ax.grid(True, dashes = [1,1], alpha = 0.25)
plt.show()
