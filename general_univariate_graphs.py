from flask import Flask, request, jsonify
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from bson import ObjectId
from io import BytesIO

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb+srv://Cristian3599:DJayts4GVRw9MTTW@proyectointeligentesii.jl6rh6d.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["ProyectoInteligentesII"]

@app.route('/general-univariate-graphs/<dataset_id>', methods=['POST'])
def generate_univariate_graphs(dataset_id):
    # Recupera el documento del dataset por su ID
    dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

    if not dataset:
        return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

    # Crear una carpeta para almacenar las imágenes
    output_folder = f"./graphs/{dataset_id}_graphs"
    os.makedirs(output_folder, exist_ok=True)

    # Convertir el conjunto de datos en un DataFrame de pandas
    df = pd.DataFrame(dataset['registros'])

    # Iterar sobre las columnas y generar gráficos
    for column in df.columns:
        # Histograma
        plt.figure()
        sns.histplot(df[column], kde=True)
        plt.title(f'Histograma de {column}')
        histogram_path = os.path.join(output_folder, f'{column}_histogram.png')
        plt.savefig(histogram_path)
        plt.close()

        # Diagrama de caja (solo para variables numéricas)
        if pd.api.types.is_numeric_dtype(df[column]):
            plt.figure()
            sns.boxplot(x=df[column])
            plt.title(f'Diagrama de Caja de {column}')
            boxplot_path = os.path.join(output_folder, f'{column}_boxplot.png')
            plt.savefig(boxplot_path)
            plt.close()
        else:
            # Gráfico de barras para columnas categóricas
            plt.figure()
            sns.countplot(x=df[column])
            plt.title(f'Distribución de Categorías en {column}')
            category_distribution_path = os.path.join(output_folder, f'{column}_category_distribution.png')
            plt.savefig(category_distribution_path)
            plt.close()

    # Crear una respuesta con las rutas de las imágenes generadas
    response_data = {
        'histogram_paths': [os.path.join(output_folder, f'{column}_histogram.png') for column in df.columns],
        'boxplot_paths': [os.path.join(output_folder, f'{column}_boxplot.png') for column in df.columns if pd.api.types.is_numeric_dtype(df[column])],
        'distribution_paths': [os.path.join(output_folder, f'{column}_distribution.png') for column in df.columns]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
