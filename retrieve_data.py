import psycopg2
import pandas as pd
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

db_params = {
    'dbname': 'FaceRecogDB',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_params)

query = 'SELECT "BM_District_Code", "BM_Taluk_Code", "BM_Beneficiary_Id_Govt", "BM_First_Name_Eng", "BM_Fat_Hus_First_Name_Eng", "BM_Scheme_Code", "BM_Address_Eng1", "BM_Photo" FROM public."BM_K2_Photo"'

df = pd.read_sql(query, conn)

conn.close()

print(df.drop(columns=['BM_Photo']))

def display_images(image_data_list):
    for image_data in image_data_list:
        image = Image.open(BytesIO(image_data))
        plt.figure()
        plt.imshow(image)
        plt.axis('off')
        plt.show()

display_images(df['BM_Photo'].tolist())
