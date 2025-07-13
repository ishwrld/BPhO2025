import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

f = 0.5

def function_x(x):
    return (-f * x) / (x - f)

def function_y(x,y):
    return (y * function_x(x)) / x

def affineTransform():
    img = cv.imread(r'Einstein.jpg')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Convert BGR to RGB for matplotlib
    height, width,_ = img.shape

    p1 = np.array([[90,10],
                  [1,10],
                  [10,90]],dtype=np.float32)
    
    p2 = np.array([[function_x(x0), function_y(x0, x1)] for x0, x1 in p1], dtype=np.float32)
    
    T = cv.getAffineTransform(p1, p2)
    imgTrans = cv.warpAffine(img, T, (width, height))  

    fig, (ax,ax2) = plt.subplots(1,2, figsize=(10, 5))
    ax.imshow(img)
    ax2.imshow(imgTrans)
    ax.set_title("Original Image")
    ax2.set_title("Transformed Image")

    plt.show()

if __name__ == "__main__":
    affineTransform()



# p2 = np.array([[90, 10],
#                [5,1],
#                [15, 80]], dtype=np.float32)