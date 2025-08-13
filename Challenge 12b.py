import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def sin(angle): # DEGREES INPUT
    return np.sin(np.deg2rad(angle))

def cos(angle): # DEGREES INPUT
    return np.cos(np.deg2rad(angle))

def tan(angle): # DEGREES INPUT
    return np.tan(np.deg2rad(angle))

def get_theta_t(alpha, theta_i, n):
    val = (n ** 2 - sin(theta_i) ** 2) ** 0.5 * sin(alpha) - sin(theta_i) * cos(alpha)
    val = np.clip(val,-1,1)
    return np.rad2deg(np.arcsin(val))

def get_delta(theta_i, n):
    return np.rad2deg(np.arcsin(sin(theta_i) / n))

def refractiveGlass(freq): # Returns n, refractive index
    wavelength = 3e8 / (freq * 1e6)
    # Sellmeier coefficients for crown glass
    coeffA = [1.03961212, 0.231792344, 1.01146945]
    coeffB = [0.00600069867, 0.0200179144, 103.560653]

    #wavelength = wavelength / 1000  # Convert to micrometres
    waveSquare = wavelength ** 2  # Wavelength squared (makes equation easier)
    sumCoeff = 0
    for index in range(len(coeffA)):
        sumCoeff += (coeffA[index] * waveSquare) / (waveSquare - coeffB[index])

    return (1 + sumCoeff) ** 0.5

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

# Top left
def top_left(alpha, freq):
    # IF TIME FIND MIN THETA_I PROPERLY
    global ax1
    ax1.set_title(r'$\theta_{t}$ vs $\theta_{i}$') #"Transmission angle vs Angle of Incidence")
    ax1.set_xlabel("Angle of Incidence (degrees)")
    ax1.set_ylabel("Transmission Angle (degrees)")
    ax1.set_xlim(0, 90)
    ax1.set_ylim(0, 100)
    ax1.grid(True, linestyle = '--',alpha = 0.4)

    n = refractiveGlass(freq)
    colour = 'blue' #chooseColour(freq)
    theta_i = np.linspace(0, 90, 90)
    theta_t = get_theta_t(alpha, theta_i, n)
    mask = theta_t != 90
    theta_i = theta_i[mask]
    theta_t = theta_t[mask]
    min_theta_i = theta_i.min()

    ax1.plot(theta_i, theta_t, color = colour, linewidth = 0.5)
    ax1.axvline(min_theta_i, 0, 90, color = 'red', linewidth = 0.5)

# Bottom left
def bottom_left(alpha, freq):
    global ax2
    ax2.set_title("Deflection Angle")
    ax2.set_xlabel("Angle of Incidence (degrees)")
    ax2.set_ylabel(rf"Deflection Angle  $\delta$ (degrees)")
    ax2.set_xlim(0, 90)
    ax2.set_ylim(25, 55)
    ax2.grid(True, linestyle = '--',alpha = 0.4)

    n = refractiveGlass(freq)
    colour = 'blue' #chooseColour(freq)
    theta_i = np.linspace(0, 90, 500)
    theta_t = get_theta_t(alpha, theta_i, n)
    mask = theta_t != 90
    theta_i = theta_i[mask]
    theta_t = theta_t[mask]
    min_theta_i = theta_i.min()
    delta = theta_i + theta_t - alpha

    ax2.plot(theta_i, delta, color = colour, linewidth = 0.5)
    ax2.axvline(min_theta_i, 0, 90, color = 'red', linewidth = 0.5)

# Right
def right():
    freq = 542.5
    global ax3
    ax3.set_title(rf"Deflection Angle  $\delta$ using frequency {freq} THz")
    ax3.set_xlabel("Angle of Incidence (degrees)")
    ax3.set_ylabel(rf"Deflection Angle $\delta$ (degrees)")
    ax3.set_xlim(0, 90)
    ax3.set_ylim(0, 90)
    ax3.grid(True, linestyle = '--', alpha = 0.4)

    alphas = np.arange(10, 80, 5)
    colours = np.array([chooseColour(alp*5+360) for alp in alphas])
    n = refractiveGlass(freq)

    for index in range(len(alphas)):
        alpha = alphas[index]
        colour = colours[index]
        theta_i = np.linspace(0, 90, 500)
        theta_t = get_theta_t(alpha, theta_i, n)
        mask = theta_t != 90
        theta_i = theta_i[mask]
        theta_t = theta_t[mask]
        delta = theta_i + theta_t - alpha

        ax3.plot(theta_i, delta, color = colour, linewidth = 0.5, label = rf'$\alpha = {alpha}^\circ$')
    
    # Legend to the right of ax3
    ax3.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
   

# def update(val):
#     ax1.clear()
#     ax2.clear()
#     ax3.clear()
#     alpha = alpha_slider.val
#     freq = freq_slider.val

#     top_left(alpha, freq)
#     bottom_left(alpha, freq)
#     right()

alpha = 45
freq = 542.5

fig = plt.figure(figsize=(10, 5)) 


# Subplots
ax1 = plt.subplot2grid((2, 4), (0, 0), colspan=2)        # top left (2 columns wide)
ax2 = plt.subplot2grid((2, 4), (1, 0), colspan=2)        # bottom left (2 columns wide)
ax3 = plt.subplot2grid((2, 4), (0, 2), colspan=2, rowspan=2)  # right (2 columns wide, full height)

fig.subplots_adjust(left=0.1, right=0.85, bottom=0.15, top=0.9, hspace=0.5)
#plt.tight_layout(rect=[0, 0.1, 1, 1])  # Space at bottom for slider

top_left(alpha, freq)
bottom_left(alpha, freq)
right()
pos = ax3.get_position()  # Bbox(x0, y0, width, height)
new_pos = [pos.x0 + 0.05, pos.y0, pos.width - 0.05, pos.height]  # shift right by 0.05, reduce width
ax3.set_position(new_pos)

# # Create the slider
# alpha_ax = fig.add_axes([0.75, 0.03, 0.15, 0.03])  # [left, bottom, width, height]
# alpha_slider = Slider(alpha_ax, "Alpha", 0.0, 50, valinit=alpha)

# freq_ax = fig.add_axes([0.1, 0.03, 0.15, 0.03])
# freq_slider = Slider(freq_ax, "Freq (THz)", 410, 750, valinit=freq)

# alpha_slider.on_changed(update)
# freq_slider.on_changed(update)
manager = plt.get_current_fig_manager()
manager.toolbar.pack_forget()  # Removes toolbar from Tkinter window
plt.show()

