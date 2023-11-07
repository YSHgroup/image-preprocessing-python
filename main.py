import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
from imutils import rotate_bound
from skimage.metrics import structural_similarity as ssim

def rotate_image(image):
    # Load the input image
    image = np.array(image)
    
    # Convert the image to RGB channel ordering
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print('rotate-rgb->', rgb)

    # Use Tesseract to determine the text orientation
    results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)

    # Extract the rotation angle from the orientation information
    rotation_angle = int(results["rotate"])

    # Rotate the image by the calculated angle to correct the text orientation
    rotated_image = rotate_bound(image, rotation_angle)

    return rotated_image

def enhance_image(image):
    image_array = np.array(image)
    
    denoised_image_array = cv2.fastNlMeansDenoising(image_array)
    denoised_image = Image.fromarray(denoised_image_array)
    image_array = np.array(denoised_image)
    image = Image.fromarray(np.uint8(image_array))
    # image = rotate_image(image)

    # Create an ImageEnhance object and apply the enhancement
    enhancer = ImageEnhance.Sharpness(image)
    enhanced_image = enhancer.enhance(1.5)

    # Create an enhancer object
    enhancer = ImageEnhance.Brightness(image)
    # Increase the brightness by a factor of 1.5
    enhanced_image = enhancer.enhance(1.5)
    
    # Enhance the image's contrast
    enhancer_contrast = ImageEnhance.Contrast(image)
    image = enhancer_contrast.enhance(2)
    return enhanced_image



image = Image.open('./Dataset/pess.jpg')
image = enhance_image(image)

image.show()