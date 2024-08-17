import os
import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np

model = InceptionResnetV1(pretrained='vggface2').eval()

def preprocess_image(image_path):
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img = img.resize((160, 160)) 
    img = np.array(img)
    
    if img.ndim == 2:
        img = np.expand_dims(img, axis=2)
        
    img = img / 255.0 
    img = (img - 0.5) / 0.5
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    img = torch.tensor(img, dtype=torch.float32)
    return img

def get_embeddings(image_path):
    img = preprocess_image(image_path)
    with torch.no_grad():
        embeddings = model(img)
    return embeddings

def process_images_in_folder(folder_path, output_file):
    with open(output_file, 'w') as f:
        for image_filename in os.listdir(folder_path):
            if image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, image_filename)
                embeddings = get_embeddings(image_path)
                embeddings_str = ' '.join(map(str, embeddings.squeeze().tolist()))
                f.write(f"{image_filename},{embeddings_str}\n")
                print(f"Processed: {image_filename}")

image_folder = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'
output_file = 'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1\\embeddings.txt'
process_images_in_folder(image_folder, output_file)