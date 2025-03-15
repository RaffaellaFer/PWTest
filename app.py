from flask import Flask, render_template, request, url_for, redirect 
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
from datetime import date
from datetime import datetime

# Instantiate the Flask class by creating a flask application
app = Flask(__name__)

