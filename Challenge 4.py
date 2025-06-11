from matplotlib import pyplot as plt
import math
import numpy as np

L = 2
x = np.linspace(0, L, 1000)
C = 345
n = 1
n2 = 1.5  
y = 1

def formula(x):
    return (np.sqrt((x)**2 + y**2) / (C/n)) + (np.sqrt(((L) - (x))**2 + y**2) / (C/n2))

t = formula(x)


plt.plot(x, t, linestyle='-', color='b', label='Data Points')
plt.title("Test for Snell's Law")
plt.xlabel("x (m)")
plt.ylabel("Time (s)")
plt.show()