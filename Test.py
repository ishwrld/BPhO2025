def challenge_6():
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt

    # Load image
    img = cv2.imread("Einstein.jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    # Define new canvas size (larger than original image)
    canvas_h = int(h * 1.5)
    canvas_w = int(w * 1.5)

    # Create meshgrid for the canvas
    x, y = np.meshgrid(np.arange(canvas_w), np.arange(canvas_h))

    # Shift the image right and up (into the expanded area)
    shift_x = -w // 4   # Shift left by 1/4 image width (=> into right side of canvas)
    shift_y = -h // 4   # Shift up by 1/4 image height (=> into bottom side of canvas)

    # Compute corresponding coordinates in the original image
    map_x = (x + shift_x).astype(np.float32)
    map_y = (y + shift_y).astype(np.float32)

    # Remap
    remapped = cv2.remap(
        img_rgb, map_x, map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)  # white background for out-of-bounds
    )

    # Show result
    plt.figure(figsize=(8, 8))
    plt.imshow(remapped)
    plt.title("Image shifted onto larger canvas")
    plt.axis("off")
    plt.show()

challenge_6()