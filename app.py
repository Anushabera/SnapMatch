from flask import Flask, render_template, request
import os
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch

app = Flask(__name__)

# Load the pretrained model
model = InceptionResnetV1(pretrained='vggface2').eval()

def preprocess_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((160, 160))
    image = np.array(image)
    image = image / 255.0
    image = (image - 0.5) / 0.5
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)
    image = torch.tensor(image, dtype=torch.float32)
    return image

def get_embedding(image):
    image = preprocess_image(image)
    with torch.no_grad():
        embedding = model(image)
    return embedding.squeeze().numpy()

def are_images_similar(image_a, image_b, threshold=0.8):
    emb_a = get_embedding(image_a).reshape(1, -1)
    emb_b = get_embedding(image_b).reshape(1, -1)
    similarity = cosine_similarity(emb_a, emb_b)[0][0]
    return similarity > threshold

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file1' not in request.files or 'file2' not in request.files:
        return "Please upload two images."
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    file1_path = os.path.join(upload_folder, file1.filename)
    file2_path = os.path.join(upload_folder, file2.filename)
    file1.save(file1_path)
    file2.save(file2_path)
    
    image1 = Image.open(file1_path)
    image2 = Image.open(file2_path)
    
    similar = are_images_similar(image1, image2)
    
    os.remove(file1_path)
    os.remove(file2_path)
    
    if similar:
        return "Duplicate Images"
    else:
        return "No Duplicacy"

if __name__ == '__main__':
    app.run(debug=True)
