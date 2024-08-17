##########################   database   (final code) ##########################

from flask import Flask, render_template, request, jsonify
import os
import psycopg2
from base64 import b64encode

app = Flask(__name__)

# Database connection parameters
db_params = {
    'dbname': 'FaceRecogDB',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the database
def get_db_connection():
    return psycopg2.connect(**db_params)

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch images and details based on district and taluk
@app.route('/get-images', methods=['GET'])
def get_images():
    district = request.args.get('district')
    taluk = request.args.get('taluk')
    
    if district and taluk:
        conn = get_db_connection()
        
        # Example query: Fetch images and details from database based on district and taluk
        query = 'SELECT "BM_Photo", "BM_First_Name_Eng", "BM_Scheme_Code", "BM_Address_Eng1" FROM public."BM_K2_Photo" WHERE "BM_District_Code" = %s AND "BM_Taluk_Code" = %s'
        cursor = conn.cursor()
        cursor.execute(query, (district, taluk))
        results = cursor.fetchall()
        cursor.close()
        
        conn.close()
        
        images_data = []
        
        for result in results:
            photo_data, first_name_eng, scheme_code, address_eng = result
            
            # Convert photo_data to base64 for HTML display
            image_base64 = b64encode(photo_data).decode('utf-8') if photo_data else None
            
            images_data.append({
                'image_base64': image_base64,
                'BM_First_Name_Eng': first_name_eng,
                'BM_Scheme_Code': scheme_code,
                'BM_Address_Eng1': address_eng
            })
        
        return jsonify({'images': images_data})
    
    return jsonify({'images': []})

if __name__ == '__main__':
    app.run(debug=True)






# ################################ testing ##########################

# from flask import Flask, render_template
# import psycopg2
# import csv

# app = Flask(__name__)

# # Define the CSV file with ID pairs
# input_file = "D:\\Duplicate_face_detection\\Sorted_images\\D_1_T_1\\result\\id_pairs.csv"

# # Database connection details
# db_config = {
#     'dbname': 'FaceRecogDB',
#     'user': 'postgres',
#     'password': '1234',
#     'host': 'localhost',
#     'port': '5432'
# }

# def fetch_data_from_db(id):
#     conn = psycopg2.connect(**db_config)
#     cur = conn.cursor()
#     query = """
#     SELECT "BM_First_Name_Eng", "BM_Scheme_Code", "BM_Address_Eng1", "BM_Photo"
#     FROM public."BM_K2_Photo"
#     WHERE "BM_Beneficiary_Id_Govt" = %s
#     """
#     cur.execute(query, (id,))
#     data = cur.fetchone()
#     cur.close()
#     conn.close()
#     return data

# @app.route('/')
# def index():
#     results = []
#     with open(input_file, mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             first_id = row['First_ID']
#             second_id = row['Second_ID']
#             first_data = fetch_data_from_db(first_id)
#             second_data = fetch_data_from_db(second_id)
#             results.append({
#                 'first_id': first_id,
#                 'first_data': first_data,
#                 'second_id': second_id,
#                 'second_data': second_data
#             })
#     return render_template('index.html', results=results)

# if __name__ == '__main__':
#     app.run(debug=True)
