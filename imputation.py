from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
from sklearn.impute import SimpleImputer
import json

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client["proyecto_inteligentes_II"]

@app.route('/imputation/<dataset_id>/type/<number_type>', methods=['POST'])
def impute_data(dataset_id, number_type):
    try:
        # Recupera el documento del dataset por su ID
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        # Convierte el campo 'registros' en un DataFrame de pandas
        df = pd.DataFrame(dataset['registros'])

        # Separa columnas numéricas y no numéricas
        numeric_columns = df.select_dtypes(include='number').columns
        non_numeric_columns = df.select_dtypes(exclude='number').columns

        # Realiza la imputación según el tipo seleccionado
        if number_type == '1':
            # Eliminar registros que contienen datos faltantes
            df_imputed = df.dropna()
        elif number_type == '2':
            imputer_numeric = SimpleImputer(strategy='mean')
            df_imputed = df.copy()  # Create a copy of the original DataFrame
            df_imputed[numeric_columns] = imputer_numeric.fit_transform(df[numeric_columns])

             # Imputación por moda para variables no numéricas
            imputer_non_numeric = SimpleImputer(strategy='most_frequent')
            df_imputed[non_numeric_columns] = imputer_non_numeric.fit_transform(df[non_numeric_columns])

        # Almacena los datos imputados en MongoDB Atlas como un nuevo documento
        db.imputed_data.insert_one({'registros': df_imputed.to_dict(orient='records')})

        return jsonify({'success': 'Datos imputados y almacenados exitosamente en MongoDB Atlas'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004, debug=True)
