import os
import cv2
import face_recognition
from collections import defaultdict
import csv
import matplotlib.pyplot as plt

# Directory containing the dataset of images
dataset_dir = r'D:\Duplicate_face_detection\docs\image_data'

# Initialize the face encodings dictionary
face_encodings_dict = defaultdict(list)

# Process each image in the dataset
for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(dataset_dir, filename)
        image = cv2.imread(image_path)
        
        if image is not None:
            # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect face locations and face encodings in the image
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            for encoding in face_encodings:
                face_encodings_dict[filename].append(encoding)

# Compare face encodings to find duplicates
matched_faces = defaultdict(list)
image_names = list(face_encodings_dict.keys())
processed_images = set()  # Set to keep track of already processed images

for i in range(len(image_names)):
    image1 = image_names[i]
    
    if image1 in processed_images:
        continue
    
    for j in range(i+1, len(image_names)):
        image2 = image_names[j]
        
        if image2 in processed_images:
            continue
        
        for encoding_i in face_encodings_dict[image1]:
            for encoding_j in face_encodings_dict[image2]:
                match = face_recognition.compare_faces([encoding_i], encoding_j, tolerance=0.6)
                if match[0]:
                    matched_faces[image1].append(image2)
                    processed_images.add(image2)  # Mark image2 as processed
                    break  # No need to check further once a match is found

    if matched_faces[image1]:
        processed_images.add(image1)  # Mark image1 as processed if it has any matches

# Display results and save to CSV
csv_filename = 'duplicate_faces.csv'

with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Image', 'Matches'])
    
    print("Faces appearing in multiple images:")
    for image, matches in matched_faces.items():
        if matches:
            print(f"Image {image} matches with images: {', '.join(matches)}")
            csv_writer.writerow([image, ', '.join(matches)])

            # Load and display matched images
            image1 = cv2.imread(os.path.join(dataset_dir, image))
            image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(image1_rgb)
            plt.title(f"Image: {image}")
            plt.axis('off')
            
            for match in matches:
                image2 = cv2.imread(os.path.join(dataset_dir, match))
                image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                plt.subplot(1, 2, 2)
                plt.imshow(image2_rgb)
                plt.title(f"Matches with: {match}")
                plt.axis('off')
                plt.show()
        else:
            print(f"Image {image} does not match with other images")

print(f"Results have been saved to {csv_filename}")