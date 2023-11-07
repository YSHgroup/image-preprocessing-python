import os
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
    # print('rotate-rgb->', rgb)

    # Use Tesseract to determine the text orientation
    results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)

    # Extract the rotation angle from the orientation information
    rotation_angle = int(results["rotate"])

    # Rotate the image by the calculated angle to correct the text orientation
    rotated_image = rotate_bound(image, rotation_angle)
    rotate_image = Image.fromarray(rotated_image)
    return rotate_image

def enhance_image(image):
    image_array = np.array(image)
    
    blurred = cv2.GaussianBlur(image_array, (0, 0), 3)
    sharpened = cv2.addWeighted(image_array, 1.5, blurred, -0.5, 0)
    
    denoised_image_array = cv2.fastNlMeansDenoising(sharpened)
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

def main():
    input_folder = './Dataset'
    output_folder = './output'

    if not os.path.exists(input_folder):
        os.makedirs(output_folder)
        


image = Image.open('./Dataset/pess.jpg')
image = enhance_image(image)
rotated = rotate_image(image)

rotated.show()

if __name__ == '__main__':
    main()