from flask import Flask, jsonify
from threading import Thread
from subprocess import Popen
import time

app_load = Flask(__name__)
app_statics = Flask(__name__)
app_columns = Flask(__name__)
app_imputations = Flask(__name__)
app_general_univariate_graphs = Flask(__name__)
app_univariate_graphs = Flask(__name__)
app_bivariate_graphs = Flask(__name__)
app_multivariate_graphs = Flask(__name__)
app_pca = Flask(__name__)
app_train = Flask(__name__)

load_service_process = Popen(["python", "data_loader.py"])
statics_service_process = Popen(["python", "basic_statics.py"])
columns_service_process = Popen(["python", "columns_describe.py"])
imputations_service_process = Popen(["python", "imputation.py"])
general_univariate_graphs_service_process = Popen(["python", "general_univariate_graphs.py"])
univariate_graphs_service_process = Popen(["python", "univariate_graphs.py"])
bivariate_graphs_service_process = Popen(["python", "bivariate_graphs.py"])
multivariate_graphs_service_process = Popen(["python", "multivariate_graphs.py"])
pca_service_process = Popen(["python", "pca.py"])
train_service_process = Popen(["python", "train.py"])

@app_load.route('/status')
def load_service_status():
    return jsonify({'status': 'El servicio de carga está en funcionamiento'})

@app_statics.route('/status')
def statistics_service_status():
    return jsonify({'status': 'El servicio de estadísticas está en funcionamiento'})

@app_columns.route('/status')
def columns_service_status():
    return jsonify({'status': 'El servicio de descripción de columnas está en funcionamiento'})

@app_imputations.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de imputación está en funcionamiento'})

@app_general_univariate_graphs.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de general univariate graphs está en funcionamiento'})

@app_univariate_graphs.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de univariate graphs está en funcionamiento'})

@app_bivariate_graphs.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de bivariate graphs está en funcionamiento'})

@app_multivariate_graphs.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de multivariate graphs está en funcionamiento'})

@app_pca.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de pca está en funcionamiento'})

@app_train.route('/status')
def imputations_service_status():
    return jsonify({'status': 'El servicio de train está en funcionamiento'})

def check_services_status():
    while True:
        time.sleep(5)
        if load_service_process.poll() is not None:
            print("El servicio de carga ha terminado.")
            break
        if statics_service_process.poll() is not None:
            print("El servicio de estadísticas ha terminado.")
            break
        if columns_service_process.poll() is not None:
            print("El servicio de descripción de columnas ha terminado.")
            break
        if imputations_service_process.poll() is not None:
            print("El servicio de imputación ha terminado.")
            break
        if general_univariate_graphs_service_process.poll() is not None:
            print("El servicio de general univariate graphs ha terminado.")
            break
        if univariate_graphs_service_process.poll() is not None:
            print("El servicio de univariate graphs ha terminado.")
            break
        if bivariate_graphs_service_process.poll() is not None:
            print("El servicio de bivariate graphs ha terminado.")
            break
        if multivariate_graphs_service_process.poll() is not None:
            print("El servicio de multivariate graphs ha terminado.")
            break
        if train_service_process.poll() is not None:
            print("El servicio de train ha terminado.")
            break

if __name__ == '__main__':
    load_thread = Thread(target=app_load.run, kwargs={'port': 5001, 'debug': True})
    statics_thread = Thread(target=app_statics.run, kwargs={'port': 5002, 'debug': True})
    columns_thread = Thread(target=app_columns.run, kwargs={'port': 5003, 'debug': True})
    imputations_thread = Thread(target=app_imputations.run, kwargs={'port': 5004, 'debug': True})
    general_univariate_graphs_thread =  Thread(target=app_general_univariate_graphs.run, kwargs={'port': 5005, 'debug': True})
    univariate_graphs_thread =  Thread(target=app_univariate_graphs.run, kwargs={'port': 5006, 'debug': True})
    bivariate_graphs_thread =  Thread(target=app_bivariate_graphs.run, kwargs={'port': 5007, 'debug': True})
    multivariate_graphs_thread =  Thread(target=app_multivariate_graphs.run, kwargs={'port': 5008, 'debug': True})
    pca_thread =  Thread(target=app_pca.run, kwargs={'port': 5009, 'debug': True})
    train_thread =  Thread(target=app_multivariate_graphs.run, kwargs={'port': 5010, 'debug': True})

    status_thread = Thread(target=check_services_status)

    load_thread.start()
    statics_thread.start()
    columns_thread.start()
    imputations_thread.start()
    status_thread.start()
    general_univariate_graphs_thread.start()
    univariate_graphs_thread.start()
    bivariate_graphs_thread.start()
    multivariate_graphs_thread.start()
    pca_thread.start()
    train_thread.start()

    load_thread.join()
    statics_thread.join()
    columns_thread.join()
    imputations_thread.join()
    status_thread.join()
    general_univariate_graphs_thread.join()
    univariate_graphs_thread.join()
    bivariate_graphs_thread.join()
    multivariate_graphs_thread.join()
    pca_thread.join()
    train_thread.join()
