import cv2
import numpy as np
import psycopg2
from psycopg2 import sql
import os
import io

# Function to enhance and save images
def enhance_and_save_images(rows, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each row (image) fetched from database
    for row in rows:
        beneficiary_id, name, image_binary = row
        
        # Load image from bytea data
        nparr = np.frombuffer(image_binary, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perform image sharpening using cv2.filter2D()
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(image, -1, kernel)
        
        # Save the sharpened image to the output folder
        output_filename = os.path.join(output_folder, f'{beneficiary_id}_{name}_sharpened.jpg')
        cv2.imwrite(output_filename, sharpened_image)
        
        print(f"Enhanced and saved: {output_filename}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="FaceRecogDB",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Query to retrieve images and necessary information
select_query = sql.SQL(
    "SELECT \"BM_Beneficiary_Id_Govt\", \"BM_First_Name_Eng\", \"BM_Photo\" FROM \"BM_K2_Photo\""
)
cursor.execute(select_query)
rows = cursor.fetchall()

# Close cursor after fetching data
cursor.close()
conn.close()

# Define output folder where enhanced images will be saved
output_folder = 'sharpened_images'

# Call the function to enhance and save images
enhance_and_save_images(rows, output_folder)
