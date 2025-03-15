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
db = client.todo


#FUNZIONE PER CREARE UNA FOODBOX
@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == "POST":
        nome = request.form.get('nome')
        contenuto = request.form.get('contenuto')
        priorita = request.form.get('priorita')
        db.todoList.insert_one({'nome': nome, 'contenuto': contenuto, 'priorita': int(priorita)})
        return redirect(url_for('home'))
    all_todos = db.todoList.find()    # display all todo documents
    return render_template('home.html', todos = all_todos) # render home page template with all todos

if __name__ == "__main__":
    app.run(debug=True) #running your server on development mode, setting debug to True