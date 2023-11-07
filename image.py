import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pytesseract
from imutils import rotate_bound
from skimage.metrics import structural_similarity as ssim

def detect_tilted_image(image: Image):
    image = np.array(image)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray:', gray)
    cv2.waitKey(0)
    # Apply thresholding to the image
    
    gray=pytesseract.image_to_string(np.array(gray))
    
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print('threshold-->', threshold)
    # threshold = np.array(threshold)
    cv2.imshow('threhold:', threshold)
    # Perform OCR on the thresholded image
    text = pytesseract.image_to_osd(threshold)

    # Extract the rotation angle from the OCR result
    # angle = int(text.split('Rotate: ')[-1])
    text = text.split('Rotate: ')[-1].split('\n', 1)[0]
    angle = int(text.strip())
    
    #     # Perform adaptive thresholding to preprocess the image
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #                                cv2.THRESH_BINARY_INV, blockSize=15, C=2)

    # # Invert the image
    # inverted = cv2.bitwise_not(thresh)

    # # Use pytesseract to extract text from the image
    # data = pytesseract.image_to_osd(inverted)

    # # Extract the rotation angle from the OCR output
    # angle = int(data.split("Rotate: ")[-1])

    return angle

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

# Load the image
# image = Image.open('./Dataset/A & W Sinclair Ltd/fa7ed6d7-a7e4-4798-a5d7-45d50c717618.jpeg')
image = Image.open('./Dataset/A Ross and Sons/480a1af9-cdac-4ca3-b39b-ed407beab97c.jpeg')
image.show()
# Call the function to stand the image upright
upright_image = detect_tilted_image(image)
print('angle-->', upright_image)

image = np.array(image)
rotated_image = rotate_bound(image, upright_image)
cv2.imshow('im--', rotated_image)
cv2.waitKey(0)
# Display or save the upright image
# upright_image.show()

# image = Image.open('./Dataset/A Ross and Sons/4c2727d0-0c4c-472c-804c-e855a1e353ab.jpeg')
# image = enhance_image(image)
# rotated = stand_image_upright(image)
# # image.show()have

# if rotated != None:
#   rotated.show()