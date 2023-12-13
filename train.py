from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import os

app = Flask(__name__)

mongo_uri = "mongodb+srv://Cristian3599:DJayts4GVRw9MTTW@proyectointeligentesii.jl6rh6d.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["ProyectoInteligentesII"]

def train_models(X_train, y_train, algorithms):
    trained_models = []

    for algorithm in algorithms:
        if algorithm == 1:
            model = LogisticRegression()
        elif algorithm == 2:
            model = KNeighborsClassifier()
        elif algorithm == 3:
            model = SVC()
        elif algorithm == 4:
            model = GaussianNB()
        elif algorithm == 5:
            model = DecisionTreeClassifier()
        elif algorithm == 6:
            model = MLPClassifier()

        model.fit(X_train, y_train)
        trained_models.append(model)

    return trained_models

def perform_hold_out_split(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test

def perform_cross_validation(X, y, folds=5):
    # Esta función podría ser mejorada según tus necesidades específicas
    return cross_val_score(LogisticRegression(), X, y, cv=folds)

def apply_normalization(X, normalization_type):
    if normalization_type == 1:
        scaler = MinMaxScaler()
    elif normalization_type == 2:
        scaler = StandardScaler()

    X_normalized = scaler.fit_transform(X)
    return X_normalized

@app.route('/train/<dataset_id>/', methods=['POST'])
def train_models_endpoint(dataset_id):
    try:
        dataset = db.load.find_one({'_id': ObjectId(dataset_id)})

        if not dataset:
            return jsonify({'error': 'No se encontró el dataset con el ID proporcionado'}), 404

        df = pd.DataFrame(dataset['registros'])

        # Extraer los campos del body de la petición
        body = request.json
        algorithms = body.get('algorithms', [])
        option_train = body.get('option_train', 1)
        normalization = body.get('normalization', 1)
        target_column = body.get('target_column')

        if target_column not in df.columns:
            return jsonify({'error': f'La columna objetivo "{target_column}" no se encuentra en el dataset'}), 400

        # Dividir el dataset en características (X) y etiquetas (y)
        X = df.drop(columns=target_column)
        y = df[target_column]

        # Aplicar normalización si es necesario
        X_normalized = apply_normalization(X, normalization)

        # Dividir el dataset según la opción de entrenamiento
        if option_train == 1:
            X_train, X_test, y_train, y_test = perform_hold_out_split(X_normalized, y)
        elif option_train == 2:
            # Puedes personalizar la función de cross-validation según tus necesidades específicas
            X_train, y_train = X_normalized, y

        # Entrenar modelos
        trained_models = train_models(X_train, y_train, algorithms)

        # Guardar información del entrenamiento en la base de datos
        training_info = {
            'dataset_id': ObjectId(dataset_id),
            'models': [str(model) for model in trained_models],
            'option_train': option_train,
            'normalization': normalization,
            'target_column': target_column
        }

        training_collection = db.training_results
        result = training_collection.insert_one(training_info)

        return jsonify({'training_id': str(result.inserted_id)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5010, debug=True)
