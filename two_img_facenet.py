import torch
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the pretrained model
model = InceptionResnetV1(pretrained='vggface2').eval()

def preprocess_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((160, 160))
    img = np.array(img)
    img = img / 255.0
    img = (img - 0.5) / 0.5
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    img = torch.tensor(img, dtype=torch.float32)
    return img

def get_embedding(image_path):
    img = preprocess_image(image_path)
    with torch.no_grad():
        embedding = model(img)
    return embedding.squeeze().numpy()

def are_images_similar(image_path_a, image_path_b, threshold=0.8):
    emb_a = get_embedding(image_path_a).reshape(1, -1)
    emb_b = get_embedding(image_path_b).reshape(1, -1)
    similarity = cosine_similarity(emb_a, emb_b)[0][0]
    if similarity > threshold:
        print("Similar")
    else:
        print("Not Similar")

# Example usage
image_path_a = r'D:\Duplicate_face_detection\Test_images\original_bbox_op\boxed_equalized_image_0.jpg'
image_path_b = r'D:\Duplicate_face_detection\Test_images\original_bbox_op\boxed_equalized_image_0_1.jpg'
are_images_similar(image_path_a, image_path_b)