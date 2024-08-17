import os
import torch
import psycopg2
from psycopg2 import sql
from facenet_pytorch import InceptionResnetV1
from PIL import Image
import numpy as np
import io
from sklearn.metrics.pairwise import cosine_similarity

model = InceptionResnetV1(pretrained='vggface2').eval()

def preprocess_image(image_binary):
    img = Image.open(io.BytesIO(image_binary))
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

def get_embedding(image_binary):
    img = preprocess_image(image_binary)
    with torch.no_grad():
        embedding = model(img)
    return embedding.squeeze().numpy()

def find_duplicates(image_data, threshold=0.8):
    embeddings = {}
    for id, name, image_binary in image_data:
        embeddings[id] = get_embedding(image_binary)

    duplicates = []
    checked = set()
    image_ids = list(embeddings.keys())
    for i, id_a in enumerate(image_ids):
        for j, id_b in enumerate(image_ids):
            if i != j and (id_b, id_a) not in checked:
                checked.add((id_a, id_b))
                emb_a = embeddings[id_a].reshape(1, -1)
                emb_b = embeddings[id_b].reshape(1, -1)
                similarity = cosine_similarity(emb_a, emb_b)[0][0]
                if similarity > threshold:
                    duplicates.append((id_a, id_b, similarity))

    return duplicates

def main():
    conn = psycopg2.connect(
        dbname="FaceRecogDB",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    select_query = sql.SQL('SELECT "ID", "Name", "Photograph" FROM people_data')
    cursor.execute(select_query)
    image_data = cursor.fetchall()

    cursor.close()
    conn.close()

    duplicates = find_duplicates(image_data)
    if duplicates:
        print("Duplicate images:")
        for id_a, id_b, similarity in duplicates:
            name_a = next(image[1] for image in image_data if image[0] == id_a)
            name_b = next(image[1] for image in image_data if image[0] == id_b)
            print(f" - {name_a} and {name_b}, Similarity: {similarity:.2f}")
    else:
        print("No duplicate images")

main()
