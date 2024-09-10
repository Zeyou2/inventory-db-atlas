from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from utils.env_p import *
from inventory_handler import InventoryManager
from connect import Mongo_Manager
from datetime import datetime


db_sample = InventoryManager("central.json")
db_atlas = Mongo_Manager('inventory')
app = Flask(__name__)

# app.config["JWT_SECRET_KEY"] = "secret"

# JWTManager(app)


# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data["email"]
#     senha = data["senha"]
#     users_collection = db_atlas.get_collection('usuarios')
    
#     user = users_collection.find_one({"email" : email , "senha" : senha })
    
#     if user:
#         token = create_access_token({"id": str(user["_id"])})
#         return jsonify({"token": token}), 201
    
#     return jsonify({"error": "usuario nao existe!"}), 400

# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     return jsonify({"message": "secret"})

@app.route('/', methods=["GET", "POST"])
def index():
    colec = db_atlas.inventory.list_collection_names()
    sample = db_sample.get_collection('usuarios')
    if request.method == "POST":
        print()
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample,  redirect = redirect("/form"))

@app.route('/cadastro/<collection_name>', methods=['POST',  'GET'])
# @jwt_required()
def cadastro(collection_name):
    sample = db_sample.get_collection(collection_name)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    field = db_sample.create_form(collection_name)  
    return render_template('pages/form.html', titulo = "Inicio" , title = collection_name, collection_name = collection_name, field = field, sample = sample, view = sample, date = now )

@app.route('/send_data/<collection_name>', methods= ['POST'])
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}
    if collection_name == 'usuarios':
        form_values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
    db_sample.save_to_central(form_values, collection_name,'create')
    db_sample.insert_into_db('create')
    db_sample.delete_central()
    return redirect('/view/' + collection_name)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
def view(collection_name):
    sample = db_sample.get_collection(collection_name)
    if sample:
        return render_template('pages/view.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    return jsonify(list(sample))

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)

#     # Aqui você pode colocar a lógica de verificação de login (exemplo básico)
#     user = db_sample.get_collection('usuarios').get(email)

#     if user and user['password'] == password:  # Validação de usuário simples
#         # Cria um token JWT com o email do usuário
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"msg": "Bad username or password"}), 401
    



# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         print(email)
#         collection_name = db_atlas.inventory.list_collection_names()
#         user = collection_name.find_one()
#         if user:
#             return redirect(url_for('index')) 
#         else:
#             return redirect(url_for('login')) 

#     return render_template('pages/login.html')

