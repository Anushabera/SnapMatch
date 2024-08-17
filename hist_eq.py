from __future__ import print_function
import cv2 as cv
import os

input_folder = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'
output_folder = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.isdir(input_folder):
    print('The specified input folder does not exist:', input_folder)
    exit(0)

image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    src = cv.imread(image_path)
    
    if src is None:
        print('Could not open or find the image:', image_path)
        continue
    
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    dst = cv.equalizeHist(src_gray)

    output_image_path = os.path.join(output_folder, f'{image_file}')
    
    cv.imwrite(output_image_path, dst)
    print(f'Saved equalized image to: {output_image_path}')
