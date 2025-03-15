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

uri = "mongodb+srv://RafMosca:RafMoscaDB@cluster0.rzvmm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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

if __name__ == "__main__":
    app.run(debug=True) #running your server on development mode, setting debug to True