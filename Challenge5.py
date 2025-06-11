import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def reflect_image_across_vertical(image):
    """
    Reflects an image across a vertical mirror (x = 0).
    This is equivalent to flipping it horizontally.
    """
    return np.fliplr(image)

def plot_reflection(original, reflected):
    """
    Plots the original image and its reflected counterpart side by side.
    """
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    axs[0].imshow(original)
    axs[0].set_title("Original Image")
    axs[0].axis('off')
    
    axs[1].imshow(reflected)
    axs[1].set_title("Virtual Image (Mirror Reflection)")
    axs[1].axis('off')
    
    plt.tight_layout()
    plt.show()

def main():
    # Load image (can be PNG, JPG, etc.)
    image_path = 'object_image.png'  # Replace with your image filename
    image = mpimg.imread(image_path)
    
    # Compute virtual image
    virtual_image = reflect_image_across_vertical(image)
    
    # Plot both
    plot_reflection(image, virtual_image)

if __name__ == "__main__":
    main()
