import matplotlib.pyplot as plt
import numpy as np

u = np.arange(20,60,5)
v = np.array([65.5,40,31,27,25,23.1,21.5,20.5])
uinv = np.round(1/u,3)
vinv = np.round(1/v,3) 

plt.plot(uinv, vinv,"x", ms=5)
m, b = np.polyfit(uinv, vinv, 1)
plt.plot(uinv, m*uinv+b, color="red", label = "y = " + str(round(m,4)) + "x + " + str(round(b,4)))
plt.legend(loc="upper right")
plt.text(1, 0.9, f"f = {round(1/b,4)}",
         fontsize=12,
         ha = "right",
         va = "top",
         transform=plt.gca().transAxes)

plt.xlabel("1/u")
plt.ylabel("1/v")
plt.title("Thin lens")

manager = plt.get_current_fig_manager()
manager.toolbar.pack_forget()  # Removes toolbar from Tkinter window
plt.show()