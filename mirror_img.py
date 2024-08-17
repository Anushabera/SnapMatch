import os
from PIL import Image

def create_mirrored_image(image_path, output_path):
    try:
        img = Image.open(image_path)
        mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        mirrored_img.save(output_path)
        print(f"Saved mirrored image: {output_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_filename in os.listdir(input_folder):
        if image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, image_filename)
            
            # Get the file name without the extension and the extension separately
            file_name, file_ext = os.path.splitext(image_filename)
            
            # Create the new filename with the suffix "_a"
            new_filename = f"{file_name}_a{file_ext}"
            output_path = os.path.join(output_folder, new_filename)
            
            create_mirrored_image(image_path, output_path)

input_folder = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'
output_folder = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'

process_images_in_folder(input_folder, output_folder)
