import os
import torch
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw

mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

def detect_faces_and_draw_boxes(image_path):
    img = Image.open(image_path).convert('L')
    
    img = img.convert('RGB')
    
    boxes, _ = mtcnn.detect(img)
    
    if boxes is not None:
        draw = ImageDraw.Draw(img)
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=2)
    
    return img

image_folder = r'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'
output_folder = r'D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for image_filename in os.listdir(image_folder):
    if image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(image_folder, image_filename)
        
        img_with_boxes = detect_faces_and_draw_boxes(image_path)
        
        output_path = os.path.join(output_folder, f"{image_filename}")
        img_with_boxes.save(output_path)

        # img_with_boxes.show()

print("Face detection and bounding box drawing completed.")
