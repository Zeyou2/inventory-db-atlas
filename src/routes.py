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
    sample = db_sample.read_docs('Usuários')
    if request.method == "POST":
        print()
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample, samplev2 = samplev2, redirect = redirect("/form"))

@app.route('/cadastro/<register>', methods=['POST', 'GET'])
def cadastro(register):
    sample = db_sample.read_docs(register)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    field = db_sample.create_form(register)  
    return render_template('pages/form.html', titulo = "Inicio" , title = register, register = register, field = field, sample = sample, view = sample, date = now )

@app.route('/send_data/<register>', methods= ['POST'])
def send(register):
    values = {key: value for key, value in request.form.items()}
    if register == 'Usuários':
        values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
    db_sample.input_process(register, 'create', values)
    db_sample.insert_data('create')
    db_sample.delete_json()
    return redirect('/view/' + register)

@app.route('/view/<register>', methods=['POST', 'GET'])
def view(register):
    sample = db_sample.read_docs(register)
    return render_template('pages/view.html', titulo = "Inicio", title = register, sample = sample )
