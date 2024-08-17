import face_recognition
import psycopg2
from psycopg2 import sql
import io

def compare_faces(known_face_encodings, known_names):
    similar_faces = []
    for i in range(len(known_face_encodings)):
        for j in range(i+1, len(known_face_encodings)):
            match = face_recognition.compare_faces([known_face_encodings[i]], known_face_encodings[j])
            if match[0]:
                similar_faces.append((known_names[i], known_names[j]))
    return similar_faces

conn = psycopg2.connect(
    dbname="FaceRecogDB",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

select_query = sql.SQL(
    "SELECT \"BM_Beneficiary_Id_Govt\", \"BM_First_Name_Eng\", \"BM_Photo\" FROM \"BM_K2_Photo\""
)
cursor.execute(select_query)
rows = cursor.fetchall()

cursor.close()
conn.close()

known_face_encodings = []
known_names = []
for row in rows:
    beneficiary_id, name, image_binary = row
    image_array = face_recognition.load_image_file(io.BytesIO(image_binary))
    # Get face encodings
    face_encodings = face_recognition.face_encodings(image_array)
    if len(face_encodings) > 0:
        encoding = face_encodings[0]
        known_face_encodings.append(encoding)
        known_names.append(name)
        # print(f"Encoding dimensions for {name}: {encoding.shape}")

similar_faces = compare_faces(known_face_encodings, known_names)

if similar_faces:
    print(f"Number of similar faces detected: {len(similar_faces)}")
    print("Similar faces detected:")
    for pair in similar_faces:
        print(f" - {pair[0]} and {pair[1]}")
else:
    print("No similar faces detected.")
