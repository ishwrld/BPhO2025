from matplotlib import pyplot as plt
import numpy as np

#Refractive indexes
redN = 1.3310
orangeN = 1.3321
yellowN = 1.3327
greenN = 1.3338
cyanN = 1.3350
blueN = 1.3362
violetN = 1.3390

lw = 0.85

def primaryReflectance(angle, n):
    return 180 - 6 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) + 2 * angle

def secondaryReflectance(angle, n):
    return 4 * np.rad2deg(np.arcsin(np.sin(np.deg2rad(angle)) / n)) - 2 * angle

def primaryMinimum(n):
    return primaryReflectance(np.rad2deg(np.arcsin(((9 - n ** 2) / 8) ** 0.5)),n)

def secondaryMinimum(n):
    return secondaryReflectance(np.rad2deg(np.arcsin(((4 - n ** 2) / 3) ** 0.5)), n)

fig, ax = plt.subplots()
incident = np.arange(0, 90, 1)

#Primary rainbow
primaryRed = np.array([primaryReflectance(i, redN) for i in incident])
primaryOrange = np.array([primaryReflectance(i, orangeN) for i in incident])
primaryYellow = np.array([primaryReflectance(i, yellowN) for i in incident])
primaryGreen = np.array([primaryReflectance(i, greenN) for i in incident])
primaryCyan = np.array([primaryReflectance(i, cyanN) for i in incident])
primaryBlue = np.array([primaryReflectance(i, blueN) for i in incident])
primaryViolet = np.array([primaryReflectance(i, violetN) for i in incident])

#Secondary rainbow
secondaryRed = np.array([secondaryReflectance(i, redN) for i in incident])
secondaryOrange = np.array([secondaryReflectance(i, orangeN) for i in incident])
secondaryYellow = np.array([secondaryReflectance(i, yellowN) for i in incident])
secondaryGreen = np.array([secondaryReflectance(i, greenN) for i in incident])
secondaryCyan = np.array([secondaryReflectance(i, cyanN) for i in incident])
secondaryBlue = np.array([secondaryReflectance(i, blueN) for i in incident])
secondaryViolet = np.array([secondaryReflectance(i, violetN) for i in incident])

#Plotting primary rainbow
ax.plot(incident, primaryRed,    color='#B22222', label='Red',    linewidth=lw)  # Firebrick (warmer dark red)
ax.plot(incident, primaryOrange, color='#FF6F00', label='Orange', linewidth=lw)  # Vibrant dark orange
ax.plot(incident, primaryYellow, color='#FFEA00', label='Yellow', linewidth=lw)  # Bright warm yellow
ax.plot(incident, primaryGreen,  color='#228B22', label='Green',  linewidth=lw)  # Forest green (natural and rich)
ax.plot(incident, primaryCyan,   color='#009999', label='Cyan',   linewidth=lw)  # Muted but bright cyan
ax.plot(incident, primaryBlue,   color='#1E3A8A', label='Blue',   linewidth=lw)  # Deep royal blue
ax.plot(incident, primaryViolet, color='#7B26B9', label='Violet', linewidth=lw)  # Rich medium violet


# Plotting secondary rainbow
ax.plot(incident, secondaryRed,    color='#B22222', label='Secondary Red',    linewidth=lw)  # Firebrick
ax.plot(incident, secondaryOrange, color='#FF6F00', label='Secondary Orange', linewidth=lw)  # Vibrant dark orange
ax.plot(incident, secondaryYellow, color='#FFEA00', label='Secondary Yellow', linewidth=lw)  # Bright warm yellow (gold replaced)
ax.plot(incident, secondaryGreen,  color='#228B22', label='Secondary Green',  linewidth=lw)  # Forest green
ax.plot(incident, secondaryCyan,   color='#009999', label='Secondary Cyan',   linewidth=lw)  # Muted bright cyan
ax.plot(incident, secondaryBlue,   color='#1E3A8A', label='Secondary Blue',   linewidth=lw)  # Deep royal blue
ax.plot(incident, secondaryViolet, color='#7B26B9', label='Secondary Violet', linewidth=lw)  # Rich medium violet

# Primary minimums
primaryRedMin = ax.hlines(primaryMinimum(redN), 0, 90, colors='#B22222', linewidth=lw)  # Firebrick
primaryOrangeMin = ax.hlines(primaryMinimum(orangeN), 0, 90, colors='#FF6F00', linewidth=lw)  # Vibrant dark orange
primaryYellowMin = ax.hlines(primaryMinimum(yellowN), 0, 90, colors='#FFEA00', linewidth=lw)  # Bright warm yellow
primaryGreenMin = ax.hlines(primaryMinimum(greenN), 0, 90, colors='#228B22', linewidth=lw)  # Forest green
primaryCyanMin = ax.hlines(primaryMinimum(cyanN), 0, 90, colors='#009999', linewidth=lw)  # Muted bright cyan
primaryBlueMin = ax.hlines(primaryMinimum(blueN), 0, 90, colors='#1E3A8A', linewidth=lw)  # Deep royal blue
primaryVioletMin = ax.hlines(primaryMinimum(violetN), 0, 90, colors='#7B26B9', linewidth=lw)  # Rich medium violet

# Secondary minimums
secondaryRedMin = ax.hlines(secondaryMinimum(redN), 0, 90, colors='#B22222', linewidth=lw)  # Firebrick
secondaryOrangeMin = ax.hlines(secondaryMinimum(orangeN), 0, 90, colors='#FF6F00', linewidth=lw)  # Vibrant dark orange
secondaryYellowMin = ax.hlines(secondaryMinimum(yellowN), 0, 90, colors='#FFEA00', linewidth=lw)  # Bright warm yellow
secondaryGreenMin = ax.hlines(secondaryMinimum(greenN), 0, 90, colors='#228B22', linewidth=lw)  # Forest green
secondaryCyanMin = ax.hlines(secondaryMinimum(cyanN), 0, 90, colors='#009999', linewidth=lw)  # Muted bright cyan
secondaryBlueMin = ax.hlines(secondaryMinimum(blueN), 0, 90, colors='#1E3A8A', linewidth=lw)  # Deep royal blue
secondaryVioletMin = ax.hlines(secondaryMinimum(violetN), 0, 90, colors='#7B26B9', linewidth=lw)  # Rich medium violet

ax.set_xlim(0, 90)
ax.set_ylim(0, 180)
ax.set_title("Primary and Secondary Rainbows")
ax.set_xlabel("Incident Angle θ (degrees)")
ax.set_ylabel("Reflected angle ε (degrees)")
ax.grid(True, linestyle = '--', alpha = 0.4)
manager = plt.get_current_fig_manager()
manager.toolbar.pack_forget()  # Removes toolbar from Tkinter window
plt.show()

