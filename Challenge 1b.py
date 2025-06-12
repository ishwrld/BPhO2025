import warnings

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection


def colored_line(x, y, c, ax, **lc_kwargs):
    """
    Plot a line with a color specified along the line by a third value.

    It does this by creating a collection of line segments. Each line segment is
    made up of two straight lines each connecting the current (x, y) point to the
    midpoints of the lines connecting the current point with its two neighbors.
    This creates a smooth line with no gaps between the line segments.

    Parameters
    ----------
    x, y : array-like
        The horizontal and vertical coordinates of the data points.
    c : array-like
        The color values, which should be the same size as x and y.
    ax : Axes
        Axis object on which to plot the colored line.
    **lc_kwargs
        Any additional arguments to pass to matplotlib.collections.LineCollection
        constructor. This should not include the array keyword argument because
        that is set to the color argument. If provided, it will be overridden.

    Returns
    -------
    matplotlib.collections.LineCollection
        The generated line collection representing the colored line.
    """
    if "array" in lc_kwargs:
        warnings.warn('The provided "array" keyword argument will be overridden')

    # Default the capstyle to butt so that the line segments smoothly line up
    default_kwargs = {"capstyle": "butt"}
    default_kwargs.update(lc_kwargs)

    # Compute the midpoints of the line segments. Include the first and last points
    # twice so we don't need any special syntax later to handle them.
    x = np.asarray(x)
    y = np.asarray(y)
    x_midpts = np.hstack((x[0], 0.5 * (x[1:] + x[:-1]), x[-1]))
    y_midpts = np.hstack((y[0], 0.5 * (y[1:] + y[:-1]), y[-1]))

    # Determine the start, middle, and end coordinate pair of each line segment.
    # Use the reshape to add an extra dimension so each pair of points is in its
    # own list. Then concatenate them to create:
    # [
    #   [(x1_start, y1_start), (x1_mid, y1_mid), (x1_end, y1_end)],
    #   [(x2_start, y2_start), (x2_mid, y2_mid), (x2_end, y2_end)],
    #   ...
    # ]
    coord_start = np.column_stack((x_midpts[:-1], y_midpts[:-1]))[:, np.newaxis, :]
    coord_mid = np.column_stack((x, y))[:, np.newaxis, :]
    coord_end = np.column_stack((x_midpts[1:], y_midpts[1:]))[:, np.newaxis, :]
    segments = np.concatenate((coord_start, coord_mid, coord_end), axis=1)

    lc = LineCollection(segments, **default_kwargs)
    lc.set_array(c)  # set the colors of each segment

    return ax.add_collection(lc)


def formula(frequency):
    return (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5

def chooseColour(freq):
    if freq < 405:  # Lower than red
        return [np.nan, np.nan, np.nan]
    elif freq < 480:
        return [1,0,0]  # Red
    elif freq < 510:
        return [1, 127/255, 0]  # Orange
    elif freq < 530:
        return [1, 1, 0]  # Yellow
    elif freq < 600:
        return [0, 1, 0]  # Green
    elif freq < 620:
        return [0, 1, 1]  # Cyan    
    elif freq < 680:
        return [0, 0, 1]  # Blue
    elif freq < 790:
        return [127/255, 0, 1]  # Violet
    else:
        return [np.nan, np.nan, np.nan]

    # rgb = np.empty((freqs.size))
    # rgb[(freqs >= 405) & (freqs < 480)] = [1]                 # Red
    # rgb[(freqs >= 480) & (freqs < 510)] = [0.85]           # Orange
    # rgb[(freqs >= 510) & (freqs < 530)] = [0.72]                 # Yellow
    # rgb[(freqs >= 530) & (freqs < 600)] = [0.6]                 # Green
    # rgb[(freqs >= 600) & (freqs < 620)] = [0.35]                 # Cyan
    # rgb[(freqs >= 620) & (freqs < 680)] = [0.13]                 # Blue
    # rgb[(freqs >= 680) & (freqs <= 790)] = [(10270/11000+freqs*(-13/11000))]          # Violet

    # return rgb

    


# -------------- Create and show plot --------------
# Some arbitrary function that gives x, y, and color values
frequencies = np.linspace(390, 800, 1000)
n = formula(frequencies)
colour = np.array([chooseColour(f) for f in frequencies])

# ax = plt.subplots()
# plt.plot(frequencies, n)
# plt.title("Refractive Index of Crown Glass")
# plt.xlabel("Wavelength (nm)")
# plt.ylabel("Refractive index, n")

# Create a figure and plot the line on it
fig, ax = plt.subplots()
for i in range(len(frequencies) - 1):
    if not np.isnan(colour[i]).any():
        ax.plot(frequencies[i:i+2], n[i:i+2], color=colour[i], linewidth=2)
#lines = colored_line(frequencies, n, colour, ax1, linewidth=5, cmap="rainbow")
#fig1.colorbar(lines)  # add a color legend

# Set the axis limits and tick positions
ax.set_xlim(frequencies.min(), frequencies.max())
ax.set_ylim(n.min(), n.max())
ax.set_title("Refractive index of water")
ax.set_xlabel("Frequency (THz)")
ax.set_ylabel("Refractive index, n")

plt.show()    

