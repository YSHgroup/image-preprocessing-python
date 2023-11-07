import os
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

    # Apply thresholding to the image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Perform OCR on the thresholded image
    text = pytesseract.image_to_osd(threshold)

    # Extract the rotation angle from the OCR result
    # angle = int(text.split('Rotate: ')[-1])
    text = text.split('Rotate: ')[-1].split('\n', 1)[0]
    angle = int(text.strip())
    # print('angle-->', angle)
    return angle


def rotate_image(image):
    # # Load the input image
    image = np.array(image)
    
    # # Convert the image to RGB channel ordering
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    try:
        # Use Tesseract to determine the text orientation
        results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)

        # Extract the rotation angle from the orientation information
        rotation_angle = int(results["rotate"])
        
        # rotation_angle = detect_tilted_image(image)
        # Rotate the image by the calculated angle to correct the text orientation
        rotated_image = rotate_bound(image, rotation_angle)
        print('no error handled')
        rotate_image = Image.fromarray(rotated_image)
    except:
        # If Tesseract can't detect the orientation, assume it's not tilted
        rotated_image = rotate_bound(image, 0)
        print('error handled')
        rotate_image = Image.fromarray(rotated_image)
    finally: 
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

def image_save(path: str, image):
    # slashes = path.count('/') + path.count('\\')
    last_backslash = path.rfind('\\')
    last_slash = path.rindex('/')
    last_point = max(last_backslash, last_slash)
    sliced = path[:last_point]
    if not os.path.exists(sliced):
        os.makedirs(sliced)
    # print('slashes-->', slashes, path, sliced)
    # cv2.imwrite(path, image)
    image.save(path)

def path_recursion(input_path: str):
    # image_array = []
    for item in os.listdir(input_path):
        path_conbined = os.path.join(input_path, item)
        if os.path.isdir(path_conbined):
            print('in folder-->', path_conbined)
            path_recursion(path_conbined)
        if item.endswith(('.jpg', '.jpeg', 'png')):
            print('file-->', path_conbined)
            image = Image.open(path_conbined)
            enhanced_rotated = rotate_image(image)
            enhanced = enhance_image(enhanced_rotated)
            output_path = './output' + path_conbined.replace('./Dataset', '')
            image_save(output_path, enhanced)
            

def main():
    input_folder = './Dataset'
    output_folder = './output'

    if not os.path.exists(input_folder):
        os.makedirs(output_folder)

    # image_array = []
    # folder_array = []
    # images_in_folder = []
    path_recursion(input_folder)


if __name__ == '__main__':
    main()