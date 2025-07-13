import os 
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

f = 0.5
import matplotlib.transforms as mtransforms

fig, ax = plt.subplots()

img = cv.imread(r'Einstein.jpg')

height, width = img.shape

