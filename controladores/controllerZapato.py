from app import app, zapatos
from flask import request, render_template, redirect
import pymongo
from werkzeug.utils import secure_filename
import os
from bson.objectid import ObjectId

# --- RUTA INICIAL / LISTAR ZAPATOS ---
@app.route("/")
def inicio():
    try:
        listaZapatos = zapatos.find()
        return render_template("index.html", listaZapatos=listaZapatos)
    except pymongo.errors as error:
        return render_template("index.html", mensaje=str(error))

# --- CONSULTAR POR CÓDIGO (Validación) ---
def consultarZapatoPorCodigo(codigo):
    try:
        consulta = {"codigo": codigo}
        zapato = zapatos.find_one(consulta)
        return zapato is not None
    except pymongo.errors as error:
        print(error)
        return False

# --- MOSTRAR FORMULARIO AGREGAR ---
@app.route("/frmAgregarZapato")
def vistaAgregarZapato():
    return render_template("frmAgregarZapato.html", zapato={}, mensaje="")

# --- AGREGAR ZAPATO ---
@app.route("/agregarZapato", methods=["POST"])
def agregarZapato():
    try:
        mensaje = ""
        codigo = int(request.form["txtCodigo"])
        marca = request.form["txtMarca"]
        modelo = request.form["txtModelo"]
        precio = int(request.form["txtPrecio"])
        talla = int(request.form["txtTalla"])
        categoria = request.form["cbCategoria"]

        archivo = request.files["fileFoto"]
        nombreArchivo = secure_filename(archivo.filename)
        listaNombreArchivo = nombreArchivo.rsplit(".", 1)
        extension = listaNombreArchivo[1].lower()

        zapato = {
            "codigo": codigo,
            "marca": marca,
            "modelo": modelo,
            "precio": precio,
            "talla": talla,
            "categoria": categoria
        }

        # Validar si ya existe
        if consultarZapatoPorCodigo(codigo):
            mensaje = "Ya existe un zapato registrado con ese código"
            return render_template("frmAgregarZapato.html", zapato=zapato, mensaje=mensaje)
        else:
            resultado = zapatos.insert_one(zapato)
            if resultado.acknowledged:
                idZapato = resultado.inserted_id
                nuevoNombre = str(idZapato) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nuevoNombre))
                return redirect("/")
    except pymongo.errors as error:
        return render_template("frmAgregarZapato.html", zapato=zapato, mensaje=str(error))

# --- CONSULTAR POR ID (Para editar) ---
@app.route("/consultar/<string:idZapato>", methods=["GET"])
def consultarPorId(idZapato):
    try:
        idObj = ObjectId(idZapato)
        consulta = {"_id": idObj}
        zapato = zapatos.find_one(consulta)
        return render_template("frmEditarZapato.html", zapato=zapato)
    except pymongo.errors as error:
        listaZapatos = zapatos.find()
        return render_template("index.html", mensaje=str(error), listaZapatos=listaZapatos)

# --- ACTUALIZAR ZAPATO ---
@app.route("/actualizar", methods=["POST"])
def actualizarZapato():
    try:
        codigo = int(request.form["txtCodigo"])
        marca = request.form["txtMarca"]
        modelo = request.form["txtModelo"]
        precio = int(request.form["txtPrecio"])
        talla = int(request.form["txtTalla"])
        categoria = request.form["cbCategoria"]
        idZapato = ObjectId(request.form["idZapato"])

        criterio = {"_id": idZapato}
        datosActualizar = {
            "codigo": codigo,
            "marca": marca,
            "modelo": modelo,
            "precio": precio,
            "talla": talla,
            "categoria": categoria
        }

        consulta = {"$set": datosActualizar}
        resultado = zapatos.update_one(criterio, consulta)

        if resultado.acknowledged:
            archivo = request.files["fileFoto"]
            if archivo.filename != "":
                nombreArchivo = secure_filename(archivo.filename)
                listaNombreArchivo = nombreArchivo.rsplit(".", 1)
                extension = listaNombreArchivo[1].lower()
                nombreArchivoActualizar = str(idZapato) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivoActualizar))
            return redirect("/")
    except pymongo.errors as error:
        listaZapatos = zapatos.find()
        return render_template("index.html", mensaje=str(error), listaZapatos=listaZapatos)

# --- ELIMINAR ZAPATO ---
@app.route("/eliminar/<string:idZapato>", methods=["GET"])
def eliminarZapato(idZapato):
    try:
        idObj = ObjectId(idZapato)
        consulta = {"_id": idObj}
        resultado = zapatos.delete_one(consulta)
        return redirect("/")
    except pymongo.errors as error:
        listaZapatos = zapatos.find()
        return render_template("index.html", mensaje=str(error), listaZapatos=listaZapatos)