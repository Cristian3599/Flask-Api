from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import json

app = Flask(__name__)

mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client["proyecto_inteligentes_II"]

@app.route('/columns-describe/<dataset_id>', methods=['GET'])
def get_columns_description(dataset_id):
    try:
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        df = pd.DataFrame(dataset['registros'])

        column_types = df.dtypes.to_dict()

        data_types_mapping = {
            'object': 'Texto',
            'int64': 'Numérico',
            'float64': 'Numérico'
        }

        column_types_mapped = {col: data_types_mapping[str(dtype)] for col, dtype in column_types.items()}

        return jsonify(column_types_mapped), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True) 
