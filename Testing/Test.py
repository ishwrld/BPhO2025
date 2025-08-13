import numpy as np
import matplotlib.pyplot as plt

def plot_rainbow(ax, antisolar_elev, radius_deg, label, color):
    """
    Plot a rainbow arc centered at the antisolar point below the horizon.
    Args:
        ax: matplotlib axis
        antisolar_elev: elevation angle of antisolar point (negative)
        radius_deg: angular radius of the rainbow (42 or 51 degrees)
        label: label for the legend
        color: color of the arc
    """
    # Angle around the antisolar point in degrees (0 to 360)
    theta = np.linspace(0, 360, 1000)
    
    # Convert to radians for calculations
    theta_rad = np.radians(theta)
    
    # Cartesian coordinates of the full circle centered at (0, antisolar_elev)
    x = radius_deg * np.cos(theta_rad)
    y = antisolar_elev + radius_deg * np.sin(theta_rad)
    
    # We only want to plot the part of the arc above horizon (y >= 0)
    mask = y >= 0
    
    # Plot only continuous segments above horizon to avoid lines crossing below horizon
    # We'll break the arc into continuous segments where mask is True
    
    # Find indices where mask changes (True <-> False)
    changes = np.diff(mask.astype(int))
    idx_changes = np.where(changes != 0)[0] + 1
    
    # Split indices for continuous segments
    segments = np.split(np.arange(len(theta)), idx_changes)
    
    for seg in segments:
        if np.all(mask[seg]):
            ax.plot(x[seg], y[seg], color=color, label=label)
            label = None  # Only label the first segment for legend

def plot_model(solar_elevations):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)
    axs = axs.flatten()

    for i, h in enumerate(solar_elevations):
        ax = axs[i]
        
        antisolar = -h  # antisolar point elevation
        
        # Plot horizon line at 0 elevation
        ax.axhline(0, color='black', linewidth=1)
        
        # Plot antisolar point
        ax.plot(0, antisolar, 'ko', label='Antisolar Point')
        
        # Plot primary rainbow (radius ~42 degrees)
        plot_rainbow(ax, antisolar, 42, 'Primary Rainbow (42°)', 'blue')
        
        # Plot secondary rainbow (radius ~51 degrees)
        plot_rainbow(ax, antisolar, 51, 'Secondary Rainbow (51°)', 'red')
        
        ax.set_title(f'Solar Elevation = {h}°')
        ax.set_xlabel('Horizontal Angle (degrees)')
        ax.set_ylabel('Elevation (degrees)')
        ax.set_xlim(-60, 60)
        ax.set_ylim(-50, 70)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper right')
    
    plt.suptitle('Primary and Secondary Rainbows at Different Solar Elevations', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Solar elevations to model
solar_elevations = [5, 20, 30, 40]

# plot_model(solar_elevations)

R = 200
H = 20

def get_xlim(eps, alp):
    return (-np.cos(eps) * np.sin(alp) *  
            (R ** 2 * np.sin(eps - alp) + 2 * H * R) + H ** 2) ** 0.5

def get_xlim2(eps, alp):
    return (R ** 2 * np.sin(eps - alp) * np.sin(eps + alp) + 
            2 * H * R * np.cos(eps) * np.sin(alp) - H ** 2) ** 0.5

print(get_xlim(np.deg2rad(42),np.deg2rad(10)))
print(get_xlim2(np.deg2rad(42),np.deg2rad(10)))
