from flask import Flask, render_template, request, redirect, url_for
from utils.env_p import *
from inventory_handler import InventoryManager
from connect import Mongo_Manager
from datetime import datetime


db_sample = InventoryManager("central.json")
db_atlas = Mongo_Manager('db_invenctory')
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    colec = db_atlas.invenctory.list_collection_names()
    sample = db_sample.get_collection('Usuários')
    if request.method == "POST":
        print()
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample,  redirect = redirect("/form"))

@app.route('/cadastro/<collection_name>', methods=['POST', 'GET'])
def cadastro(collection_name):
    sample = db_sample.get_collection(collection_name)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    field = db_sample.create_form(collection_name)  
    return render_template('pages/form.html', titulo = "Inicio" , title = collection_name, collection_name = collection_name, field = field, sample = sample, view = sample, date = now )

@app.route('/send_data/<collection_name>', methods= ['POST'])
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}
    if collection_name == 'Usuários':
        form_values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
    db_sample.save_to_central(form_values, collection_name,'create')
    db_sample.insert_into_db('create')
    db_sample.delete_central()
    return redirect('/view/' + collection_name)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
def view(collection_name):
    sample = db_sample.get_collection(collection_name)
    return render_template('pages/view.html', titulo = "Inicio", title = collection_name, sample = sample )


