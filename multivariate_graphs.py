from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

mongo_uri = "mongodb+srv://Cristian3599:DJayts4GVRw9MTTW@proyectointeligentesii.jl6rh6d.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["ProyectoInteligentesII"]

def generate_correlation_plot(df, folder_path):
    os.makedirs(folder_path, exist_ok=True)

    # Filtrar solo las columnas numéricas para el gráfico de correlación
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation_df = df[numeric_columns]

    # Generar y guardar el gráfico de correlación
    correlation_plot = sns.heatmap(correlation_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    correlation_plot_path = os.path.join(folder_path, 'correlation_plot.png')
    correlation_plot.figure.savefig(correlation_plot_path)
    plt.close()

    return correlation_plot_path

@app.route('/multivariate-graphs-class/<dataset_id>/', methods=['GET'])
def generate_multivariate_graph(dataset_id):
    try:
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        df = pd.DataFrame(dataset['registros'])

        # Crear una carpeta para almacenar el gráfico de correlación (si no existe)
        folder_path = os.path.join(os.getcwd(), f'dataset_{dataset_id}_graphs')
        correlation_plot_path = generate_correlation_plot(df, folder_path)

        return jsonify({'correlation_plot_path': correlation_plot_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5008, debug=True)
