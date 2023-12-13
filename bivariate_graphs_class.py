from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Configuración de la conexión a MongoDB Atlas
mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)
db = client["proyecto_inteligentes_II"]

# Mock data de enlaces a los gráficos pair plot
graficos_pair_plot = {
    'dataset1': 'http://servidor/grafico1.png',
    'dataset2': 'http://servidor/grafico2.png',
    # Agrega más datos según sea necesario
}

@app.route('/bivariate-graphs-class/<dataset_id>', methods=['GET'])
def obtener_enlace_grafico(dataset_id):
    # Recupera el documento del dataset por su ID
    dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

    if not dataset:
        return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

    # Verificar si existe el dataset_id en los datos mock
    if dataset_id in graficos_pair_plot:
        enlace_grafico = graficos_pair_plot[dataset_id]
        return jsonify({'enlace_grafico': enlace_grafico})
    else:
        return jsonify({'error': 'Dataset no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=5007, debug=True)