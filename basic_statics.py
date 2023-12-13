from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import json

app = Flask(__name__)

mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client["proyecto_inteligentes_II"]

@app.route('/basic_statics/<dataset_id>', methods=['GET'])
def get_basic_statics(dataset_id):
    try:
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        df = pd.DataFrame(dataset['registros'])

        statistics = df.describe().to_dict()

        return jsonify(statistics), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True) 
