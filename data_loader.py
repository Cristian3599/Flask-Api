from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import json

app = Flask(__name__)

mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client["proyecto_inteligentes_II"]

@app.route('/load', methods=['POST'])
def load_data():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400

        file = request.files['file']

        allowed_extensions = {'xls', 'xlsx', 'csv'}
        if not file.filename.split('.')[-1] in allowed_extensions:
            return jsonify({'error': 'Formato de archivo no válido. Se esperaba un archivo Excel o CSV'}), 400

        if file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            return jsonify({'error': 'Formato de archivo no admitido'}), 400

        json_data = json.loads(df.to_json(orient='records'))
        db.load.insert_one({'registros': json_data})

        return jsonify({'success': 'Datos cargados exitosamente en MongoDB Atlas'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True) 