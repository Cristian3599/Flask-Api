from flask import Flask, jsonify
from threading import Thread
from subprocess import Popen
import time

app_load = Flask(__name__)
app_statics = Flask(__name__)
app_columns = Flask(__name__)
app_imputations = Flask(__name__)
app_graphs = Flask(__name__)
#app_bivariate_graphs = Flask(__name__)
app_pca = Flask(__name__)

load_service_process = Popen(["python", "data_loader.py"])
statics_service_process = Popen(["python", "basic_statics.py"])
columns_service_process = Popen(["python", "columns_describe.py"])
imputations_service_process = Popen(["python", "imputation.py"])
general_univariate_graphs_process = Popen(["python", "general_univariate_graphs.py"])
#bivariate_graphs_process = Popen(["python", "bivariate_graphs_class.py"])
pca_process = Popen(["python", "pca.py"])

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
    return jsonify({'status': 'El servicio de descripción de columnas está en funcionamiento'})

@app_graphs.route('/status')
def general_univariate_graphs_status():
    return jsonify({'status': 'El servicio de creación de gráficos está en funcionamiento'})

# @app_bivariate_graphs.route('/status')
# def bivariate_graphs_status():
#     return jsonify({'status': 'El servicio de enlace de los gráficos está en funcionamiento'})

@app_pca.route('/status')
def pca_status():
    return jsonify({'status': 'El servicio de aplicación de pca está en funcionamiento'})

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
        if general_univariate_graphs_process.poll() is not None:
            print("El servicio de creación de gráficos ha terminado.")
            break
        # if bivariate_graphs_process.poll() is not None:
        #     print("El servicio de enlace de los gráficos ha terminado.")
        #     break
        if pca_process.poll() is not None:
            print("El servicio de aplicación de pca ha terminado.")
            break

if __name__ == '__main__':
    load_thread = Thread(target=app_load.run, kwargs={'port': 5001, 'debug': True})
    statics_thread = Thread(target=app_statics.run, kwargs={'port': 5002, 'debug': True})
    columns_thread = Thread(target=app_columns.run, kwargs={'port': 5003, 'debug': True})
    imputations_thread = Thread(target=app_imputations.run, kwargs={'port': 5004, 'debug': True})
    graphs_thread = Thread(target=app_graphs.run, kwargs={'port': 5005, 'debug': True})
    #bivariate_graphs_thread = Thread(target=app_bivariate_graphs.run, kwargs={'port': 5007, 'debug': True})
    pca_thread = Thread(target=app_pca.run, kwargs={'port': 5009, 'debug': True})

    status_thread = Thread(target=check_services_status)

    load_thread.start()
    statics_thread.start()
    columns_thread.start()
    imputations_thread.start()
    graphs_thread.start()
    #bivariate_graphs_thread.start()
    pca_thread.start()
    status_thread.start()

    load_thread.join()
    statics_thread.join()
    columns_thread.join()
    imputations_thread.join()
    graphs_thread.join()
    #bivariate_graphs_thread.join()
    pca_thread.join()
    status_thread.join()
