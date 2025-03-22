# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to home home page after updating the app database
from flask import Flask, render_template, request, url_for, redirect 
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
# Instantiate the Flask class by creating a flask application
app = Flask(__name__)
# Create the mongodb client

uri = "mongodb+srv://raffafer97:raffafer97DB@cluster0.bqvzj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Database su cloud
app.config['MONGO_URI'] = 'mongodb+srv://RafMosca:RafMoscaDB@cluster0.rzvmm.mongodb.net/?retryWrites=true&w=majority'
mongo = PyMongo(app)
db = client.pharmaCenter


#FUNZIONE PER CREARE UNA FOODBOX
@app.route("/")
def home():
    return render_template('home.html') # render home page template with all farmaci

#FUNZIONE PER CREARE UNA FOODBOX
@app.route("/farmaco/", methods=('GET', 'POST'))
def farmaco():
    if request.method == "POST":
        nome = request.form.get('nome')
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.farmaci.insert_one({'nome': nome, 'tipologia': tipologia, 'tempoElaborazione': int(tempoElaborazione)})
        return redirect(url_for('farmaco'))
    all_farmaci = db.farmaci.find()    # display all todo documents
    return render_template('farmaco.html', farmaci = all_farmaci) # render home page template with all farmaci

#FUNZIONE PER CREARE UNA FOODBOX
@app.route("/farmacoView/", methods=('GET', 'POST'))
def farmacoView():
    all_farmaci = db.farmaci.find()    # display all todo documents
    return render_template('farmacoView.html', farmaci = all_farmaci) # render home page template with all farmaci

@app.route('/elimina/<oid>', methods=('POST',))
def elimina(oid):
    db.farmaci.delete_one({"_id": ObjectId(oid)})
    return redirect('/farmacoView/')

@app.route('/modificaFarmaco/<oid>', methods=('POST',))
def modificaFarmaco(oid):
    if request.method == "POST":
        nome = request.form.get('nome')
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.farmaci.update_one({"_id" : ObjectId(oid)}, {"$set": {"nome": nome, "tipologia": tipologia, "tempoElaborazione": tempoElaborazione}})
    print(nome)
    print(tipologia)
    print(tempoElaborazione)
    return redirect('/farmacoView/')

@app.route("/parametriProduzione/", methods=('GET', 'POST'))
def parametriProduzione():
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.parametriProduzione.insert_one({'tipologia': tipologia, 'tempoElaborazione': int(tempoElaborazione)})
        return redirect(url_for('parametriProduzione'))
    all_parametriProduzione = db.parametriProduzione.find()    # display all todo documents
    return render_template('parametriProduzione.html', parametriProduzione = all_parametriProduzione) # render home page template with all farmaci


@app.route("/parametriProduzioneView/", methods=('GET', 'POST'))
def parametriProduzioneView():
    all_parametriProduzioneView = db.parametriProduzione.find()    # display all todo documents
    return render_template('parametriProduzioneView.html', parametriProduzione = all_parametriProduzioneView) # render home page template with all farmaci

@app.route('/eliminaParametriProduzione/<oid>', methods=('POST',))
def eliminaParametriProduzione(oid):
    db.parametriProduzione.delete_one({"_id": ObjectId(oid)})
    return redirect('/parametriProduzioneView/')

@app.route('/modificaParametriProduzione/<oid>', methods=('POST',))
def modificaParametriProduzione(oid):
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.parametriProduzione.update_one({"_id" : ObjectId(oid)}, {"$set": {"tipologia": tipologia, "tempoElaborazione": int(tempoElaborazione)}})
    return redirect('/parametriProduzioneView/')

#FUNZIONE PER CREARE UNA FOODBOX
@app.route("/creaLotto/", methods=('GET', 'POST'))
def creaLotto():
    all_farmaci = db.farmaci.find()    # display all todo documents
    listFarmaci = list(all_farmaci)
    for farmaco in listFarmaci:
        farmaco['quantita'] = 0
    print(listFarmaci)
    return render_template('creaLotto.html', farmaci = listFarmaci) # render home page template with all farmaci

@app.route('/aggiorna_quantita', methods=['POST'])
def aggiorna_quantita():
    all_farmaci = db.farmaci.find()    # display all todo documents
    listFarmaci = list(all_farmaci)
    all_parametriProduzioneView = db.parametriProduzione.find() 
    listParametriProduzione = list(all_parametriProduzioneView)

    # Conversione in mappa
    mappaParametriProduzione = {elemento['tipologia']: elemento['tempoElaborazione'] for elemento in listParametriProduzione}

    mappa = {}

    for farmaco in listFarmaci:
        # Recupera il valore dal form usando l'ID del farmaco
        input_name = f"quantita_{farmaco['_id']}"
        nuova_quantita = request.form.get(input_name)
        
        if nuova_quantita:
            farmaco['quantita'] = int(nuova_quantita)  # Aggiorna il valore in memoria o nel database

        if farmaco['tipologia'] not in mappa:
            mappa[farmaco['tipologia']] = 0  # Inizializza il valore a 0
        mappa[farmaco['tipologia']] += int(farmaco['tempoElaborazione']) * int(farmaco['quantita'])


    # Reindirizza o restituisci una risposta

    print("mappa", mappa)
    print('')
    print(listFarmaci)
    print('')
    print(listParametriProduzione)

    for param in listParametriProduzione:
        if mappa[param["tipologia"]] > mappaParametriProduzione[param["tipologia"]]:
            print("errore")
    
    return redirect('/creaLotto/')

if __name__ == "__main__":
    app.run(debug=True) #running your server on development mode, setting debug to True