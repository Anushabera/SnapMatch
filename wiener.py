import os
import cv2
import numpy as np
from scipy.signal import wiener
import matplotlib.pyplot as plt

def enhance_image(image):
    enhanced_image = wiener(image)
    return enhanced_image

def process_images_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            image_path = os.path.join(folder_path, file)

            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                print(f'Error: Unable to load image {image_path}')
                continue
            
            enhanced_image = enhance_image(image)
            
            plt.figure(figsize=(12, 6))

            plt.subplot(1, 2, 1)
            plt.title('Original Image')
            plt.imshow(image, cmap='gray')
            plt.axis('off')

            plt.subplot(1, 2, 2)
            plt.title('Enhanced Image with Wiener Filter')
            plt.imshow(enhanced_image, cmap='gray')
            plt.axis('off')

            plt.show()

            enhanced_image_path = os.path.join(folder_path, f'enhanced_{file}')
            cv2.imwrite(enhanced_image_path, enhanced_image)

folder_path = 'D:\Duplicate_face_detection\output_images'

process_images_in_folder(folder_path)
