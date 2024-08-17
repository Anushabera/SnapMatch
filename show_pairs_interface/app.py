from flask import Flask, render_template
import psycopg2
import csv

app = Flask(__name__)

# Define the CSV file with ID pairs
input_file = "D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1\\result\\id_pairs.csv"

# Database connection details
db_config = {
    'dbname': 'FaceRecogDB',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

import base64

def fetch_data_from_db(id):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    query = """
    SELECT "BM_First_Name_Eng", "BM_Scheme_Code", "BM_Address_Eng1", "BM_Photo"
    FROM public."BM_K2_Photo"
    WHERE "BM_Beneficiary_Id_Govt" = %s
    """
    cur.execute(query, (id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data:
        # Convert memoryview to base64 string
        image_data = base64.b64encode(data[3]).decode('utf-8') if data[3] else None
        return (data[0], data[1], data[2], image_data)
    return None


@app.route('/')
def index():
    results = []
    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_id = row['First_ID']
            second_id = row['Second_ID']
            first_data = fetch_data_from_db(first_id)
            second_data = fetch_data_from_db(second_id)
            results.append({
                'first_id': first_id,
                'first_data': first_data,
                'second_id': second_id,
                'second_data': second_data
            })
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
