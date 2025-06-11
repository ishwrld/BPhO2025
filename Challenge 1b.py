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

def chooseColour(freqs):

    rgb = np.empty((freqs.size))
    rgb[(freqs >= 405) & (freqs < 480)] = [1]                 # Red
    rgb[(freqs >= 480) & (freqs < 510)] = [0.8]           # Orange
    rgb[(freqs >= 510) & (freqs < 530)] = [0.6]                 # Yellow
    rgb[(freqs >= 530) & (freqs < 600)] = [0.4]                 # Green
    rgb[(freqs >= 600) & (freqs < 620)] = [0.2]                 # Cyan
    rgb[(freqs >= 620) & (freqs < 680)] = [0.1]                 # Blue
    rgb[(freqs >= 680) & (freqs <= 790)] = [0]          # Violet

    return rgb

    


# -------------- Create and show plot --------------
# Some arbitrary function that gives x, y, and color values
frequencies = np.linspace(405, 790, 1000)
n = formula(frequencies)
colour = chooseColour(frequencies) 

# ax = plt.subplots()
# plt.plot(frequencies, n)
# plt.title("Refractive Index of Crown Glass")
# plt.xlabel("Wavelength (nm)")
# plt.ylabel("Refractive index, n")

# Create a figure and plot the line on it
fig1, ax1 = plt.subplots()
lines = colored_line(frequencies, n, colour, ax1, linewidth=10, cmap="rainbow")
fig1.colorbar(lines)  # add a color legend

# Set the axis limits and tick positions
ax1.set_xlim(frequencies.min(), frequencies.max())
ax1.set_ylim(n.min(), n.max())
ax1.set_title("Refractive index of water")
ax1.set_xlabel("Frequency (THz)")
ax1.set_ylabel("Refractive index, n")

plt.show()    

