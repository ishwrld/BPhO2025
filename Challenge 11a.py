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
ax.plot(incident, primaryRed, color='darkred', label='Red', linewidth=lw)
ax.plot(incident, primaryOrange, color='darkorange', label='Orange', linewidth=lw)
ax.plot(incident, primaryYellow, color='yellow', label='Yellow', linewidth=lw)
ax.plot(incident, primaryGreen, color='darkgreen', label='Green', linewidth=lw)
ax.plot(incident, primaryCyan, color='darkcyan', label='Cyan', linewidth=lw)
ax.plot(incident, primaryBlue, color='darkblue', label='Blue', linewidth=lw)
ax.plot(incident, primaryViolet, color='darkviolet', label='Violet', linewidth=lw)

#Plotting secondary rainbow
ax.plot(incident, secondaryRed, color='darkred', label='Secondary Red', linewidth=lw)
ax.plot(incident, secondaryOrange, color='darkorange', label='Secondary Orange', linewidth=lw)
ax.plot(incident, secondaryYellow, color='gold', label='Secondary Yellow', linewidth=lw)
ax.plot(incident, secondaryGreen, color='darkgreen', label='Secondary Green', linewidth=lw)
ax.plot(incident, secondaryCyan, color='darkcyan', label='Secondary Cyan', linewidth=lw)
ax.plot(incident, secondaryBlue, color='darkblue', label='Secondary Blue', linewidth=lw)
ax.plot(incident, secondaryViolet, color='darkviolet', label='Secondary Violet', linewidth=lw)

# Primary minimums
primaryRedMin = plt.hlines(primaryMinimum(redN), 0, 90, colors='darkred', linewidth=lw)
primaryOrangeMin = plt.hlines(primaryMinimum(orangeN), 0, 90, colors='darkorange', linewidth=lw)
primaryYellowMin = plt.hlines(primaryMinimum(yellowN), 0, 90, colors='yellow', linewidth=lw)
primaryGreenMin = plt.hlines(primaryMinimum(greenN), 0, 90, colors='darkgreen', linewidth=lw)
primaryCyanMin = plt.hlines(primaryMinimum(cyanN), 0, 90, colors='darkcyan', linewidth=lw)
primaryBlueMin = plt.hlines(primaryMinimum(blueN), 0, 90, colors='darkblue', linewidth=lw)
primaryVioletMin = plt.hlines(primaryMinimum(violetN), 0, 90, colors='darkviolet', linewidth=lw)

# Secondary minimums
secondaryRedMin = plt.hlines(secondaryMinimum(redN), 0, 90, colors='darkred', linewidth=lw)
secondaryOrangeMin = plt.hlines(secondaryMinimum(orangeN), 0, 90, colors='darkorange', linewidth=lw)
secondaryYellowMin = plt.hlines(secondaryMinimum(yellowN), 0, 90, colors='gold', linewidth=lw)
secondaryGreenMin = plt.hlines(secondaryMinimum(greenN), 0, 90, colors='darkgreen', linewidth=lw)
secondaryCyanMin = plt.hlines(secondaryMinimum(cyanN), 0, 90, colors='darkcyan', linewidth=lw)
secondaryBlueMin = plt.hlines(secondaryMinimum(blueN), 0, 90, colors='darkblue', linewidth=lw)
secondaryVioletMin = plt.hlines(secondaryMinimum(violetN), 0, 90, colors='darkviolet', linewidth=lw)


ax.set_xlim(0, 90)
ax.set_ylim(0, 180)
ax.set_title("Primary and Secondary Rainbows")
ax.set_xlabel("Incident Angle (degrees)")
ax.set_ylabel("Reflected angle (degrees)")

plt.show()

