import numpy as np
import matplotlib.pyplot as plt

def challenge1A():
    resolution = 1000  # How many points plotted for the range
    wavelengthMin = 400  # In nanometres
    wavelengthMax = 800  # In nanometres

    # Sellmeier coefficients for crown glass
    b = [0.00600069867, 0.0200179144, 103.560653]
    a = [1.03961212, 0.231792344, 1.01146945]

    def calcSellmeier(wavelength, coeffA, coeffB):
        wavelength = wavelength / 1000  # Convert to micrometres
        waveSquare = wavelength ** 2  # Wavelength squared (makes equation easier)
        sumCoeff = 0
        for index in range(len(coeffA)):
            sumCoeff += (coeffA[index] * waveSquare) / (waveSquare - coeffB[index])

        return (1 + sumCoeff) ** 0.5

    wavelengths = np.linspace(400, 800, 5)
    n = calcSellmeier(wavelengths, a, b)

    plt.plot(wavelengths, n)
    plt.title("Refractive Index of Crown Glass")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Refractive index, n")
    plt.show()

challenge1A()