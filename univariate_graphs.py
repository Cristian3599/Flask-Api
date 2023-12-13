from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import json
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb+srv://Cristian3599:DJayts4GVRw9MTTW@proyectointeligentesii.jl6rh6d.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["ProyectoInteligentesII"]

def generate_graphs_for_columns(df, folder_path):
    os.makedirs(folder_path, exist_ok=True)

    for col in df.columns:
        # Verificar si la columna es numérica antes de intentar generar gráficos
        if pd.api.types.is_numeric_dtype(df[col]):
            try:
                # Generar y guardar el gráfico de caja por columna
                boxplot = df.boxplot(column=col, figsize=(10, 6))
                boxplot_path = os.path.join(folder_path, f'{col}_boxplot.png')
                plt.savefig(boxplot_path)
                plt.close()

                # Generar y guardar el gráfico de densidad por columna
                density_plot = df[col].plot(kind='kde', legend=True, figsize=(10, 6))
                density_plot_path = os.path.join(folder_path, f'{col}_density_plot.png')
                plt.savefig(density_plot_path)
                plt.close()

            except Exception as e:
                print(f"Error al generar gráficos para la columna {col}: {str(e)}")

    return folder_path

@app.route('/univariate-graphs-class/<dataset_id>/', methods=['POST'])
def generate_univariate_graphs(dataset_id):
    try:
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        df = pd.DataFrame(dataset['registros'])

        # Crear una carpeta para almacenar los gráficos (si no existe)
        folder_path = os.path.join(os.getcwd(), f'dataset_{dataset_id}_graphs')
        result_folder_path = generate_graphs_for_columns(df, folder_path)

        return jsonify({'result_folder_path': result_folder_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5006, debug=True)