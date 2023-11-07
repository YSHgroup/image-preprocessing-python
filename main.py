import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
from skimage.metrics import structural_similarity as ssim

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


image = Image.open('./Dataset/sha.jpeg')
image = enhance_image(image)

image.show()