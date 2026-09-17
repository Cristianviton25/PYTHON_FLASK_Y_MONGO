# app.py
from flask import Flask
import pymongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/imagenes"

miConexion = pymongo.MongoClient("mongodb://localhost:27017")
baseDatos = miConexion["GESTIONZAPATOS"]
zapatos = baseDatos["ZAPATOS"]

# La importación SIEMPRE va abajo del todo para evitar la importación circular
from controladores.controllerZapato import *

if __name__ == "__main__":
    app.run(port=3000, debug=True, threaded=False, use_reloader=False)