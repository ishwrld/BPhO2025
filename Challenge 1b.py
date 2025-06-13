import matplotlib.pyplot as plt
import numpy as np

def formula(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

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

    # if freq < 405:  # Lower than red
    #     return [np.nan, np.nan, np.nan]
    # elif freq < 480:
    #     return [1,0,0]  # Red
    # elif freq < 510:
    #     return [1, 127/255, 0]  # Orange
    # elif freq < 530:
    #     return [1, 1, 0]  # Yellow
    # elif freq < 600:
    #     return [0, 1, 0]  # Green
    # elif freq < 620:
    #     return [0, 1, 1]  # Cyan    
    # elif freq < 680:
    #     return [0, 0, 1]  # Blue
    # elif freq < 790:
    #     return [127/255, 0, 1]  # Violet
    # else:
    #     return [np.nan, np.nan, np.nan]   


frequencies = np.linspace(390, 800, 1000)
n = formula(frequencies)
colour = np.array([chooseColour(f) for f in frequencies])

fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(colour[i]).any():
        ax.plot(frequencies[i:i+2], n[i:i+2], color=colour[i], linewidth=2)

ax.set_xlim(frequencies.min(), frequencies.max())
ax.set_ylim(n.min(), n.max())
ax.set_title("Refractive index of water")
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("Refractive index, n")

plt.show()    

