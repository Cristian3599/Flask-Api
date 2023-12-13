from flask import Flask, request, jsonify
from sklearn.decomposition import PCA
from pymongo import MongoClient
from bson import ObjectId
import uuid
import pandas as pd

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb+srv://Cristian3599:DJayts4GVRw9MTTW@proyectointeligentesii.jl6rh6d.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["ProyectoInteligentesII"]

def convert_strings_to_numeric(data):
    """Función para convertir cadenas numéricas a valores numéricos."""
    for i, record in enumerate(data):
        for key, value in record.items():
            if value.isdigit():
                data[i][key] = int(value)
            elif '.' in value and all(part.isdigit() for part in value.split('.')):
                data[i][key] = float(value)
            elif value == "?":
                data[i][key] = None
    return data

@app.route('/pca/<dataset_id>', methods=['POST'])
def apply_pca(dataset_id):
    # Recupera el documento del dataset por su ID
    dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

    if not dataset:
        return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

    # Obtener el conjunto de datos desde el documento
    original_dataset = dataset['registros']

    # Convertir cadenas numéricas a valores numéricos
    original_dataset = convert_strings_to_numeric(original_dataset)

    # Crear un DataFrame para manejar datos más fácilmente
    df = pd.DataFrame(original_dataset)

    # Eliminar columnas no numéricas
    df_numeric = df.select_dtypes(include=['number'])

    # Llenar valores NaN con la media
    df_numeric = df_numeric.fillna(df_numeric.mean())

    # Aplicar PCA al conjunto de datos
    pca = PCA()
    transformed_data = pca.fit_transform(df_numeric)

    # Almacenar los pesos de las componentes
    components_weights = pca.components_

    # Crear un nuevo ID para el conjunto de datos transformado
    new_dataset_id = str(ObjectId())

    # Almacenar el conjunto de datos transformado en la base de datos
    db.load.insert_one({'_id': ObjectId(new_dataset_id), 'registros': transformed_data.tolist()})

    # Preparar la respuesta
    response_data = {
        'new_dataset_id': new_dataset_id,
        'components_weights': components_weights.tolist()
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5009, debug=True)
