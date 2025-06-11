import numpy as np
import matplotlib.pyplot as plt

def challenge1B():
    resolution = 1000  # How many points plotted for the range
    freqMin = 405 #in THz
    freqMax = 790 #in THz

    
    def formula(frequency):
        n = (1 + (1 / (1.731 - (0.261 * frequency * 10 ** -3) ** 2)) ** 0.5) ** 0.5
        return n
    
    frequencies = np.linspace(freqMin, freqMax, resolution)
    n = formula(frequencies)

    plt.plot(frequencies, n)
    plt.title("Refractive index of water")
    plt.xlabel("Frequency (THz)")
    plt.ylabel("Refractive index, n")
    plt.show()




    return None

challenge1B()