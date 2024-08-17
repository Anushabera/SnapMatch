import face_recognition
import cv2
import os
import numpy as np

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            images.append(img_path)
    return images

def extract_embeddings_from_images(folder):
    image_paths = load_images_from_folder(folder)
    embeddings_list = []
    
    for img_path in image_paths:
        image = face_recognition.load_image_file(img_path)
        
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            print(f"No face detected in {img_path}")
            continue
        
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            embeddings_list.append((img_path, face_encoding))
    
    return embeddings_list

def save_embeddings_to_file(embeddings_list, output_file):
    with open(output_file, 'w') as f:
        for img_path, embedding in embeddings_list:
            f.write(f"{img_path}\n")
            np.savetxt(f, embedding.reshape(1, -1), delimiter=',')
            f.write('\n')

if __name__ == "__main__":
    input_folder = 'D:/Duplicate_face_detection/output_images/hist_eq/op_face_recog'
    output_file = 'D:/Duplicate_face_detection/embeddings+face_recog.txt'
    
    embeddings_list = extract_embeddings_from_images(input_folder)
    
    if embeddings_list:
        save_embeddings_to_file(embeddings_list, output_file)
        print(f"Face embeddings saved to {output_file}")
    else:
        print("No embeddings extracted. Check if images with faces are present in the input folder.")
