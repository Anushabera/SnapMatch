import psycopg2
from psycopg2 import sql
from PIL import Image
import io

# Function to read image file and convert to binary
def read_image(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

# Database connection parameters
conn = psycopg2.connect(
    dbname="FaceRecogDB",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Data to be inserted (multiple rows)
data_to_insert = [
    # (1, "Allen", "Akain", "Chennai", "ABC", read_image(r'C:\Users\ANUSHA BERA\Downloads\Jeff_Bezos.jpg'), "Kelambakkam", "Tamil Nadu"),
    # (2, "Bob", "Barker", "Mumbai", "XYZ", read_image(r'C:\Users\ANUSHA BERA\Downloads\flipped_photograph.jpeg'), "Navi Mumbai", "Maharashtra"),
    # (3, "Catlin", "Camelle", "Chennai City", "XYZ", read_image(r'C:\Users\ANUSHA BERA\Downloads\Edited_bezos.jpg'), "Kanchipuram", "Tamil Nadu"),
    (4, "David", "Dad", "Chennai City", "XYZ", read_image(r'D:\Duplicate_face_detection\Test_images\original_bbox_op\boxed_equalized_image_0.jpg'), "Kanchipuram", "Tamil Nadu"),
    (5, "Elle", "Ema", "Chennai City", "XYZ", read_image(r'D:\Duplicate_face_detection\Test_images\original_bbox_op\boxed_equalized_image_0.jpg'), "Kanchipuram", "Tamil Nadu"),
    # Add more rows as needed
]

# Insert image and other details into the table
insert_query = sql.SQL(
    "INSERT INTO people_data (\"ID\", \"Name\", \"Father's Name\", \"Address\", \"Scheme\", \"Photograph\", \"District\", \"State\") "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
)
cursor.executemany(insert_query, data_to_insert)

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")
