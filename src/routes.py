from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from utils.env_p import *

from inventory_handler import InventoryManager
from connect import Mongo_Manager
from datetime import datetime
import bcrypt
import base64
import json

# CRIAR COLEÇÃO de CATEGORIAS.
# CADASTRO CATEGORIAS PELA PRÓPRIA LISTA SUSPENSA.
# TIRAR SENHA DA VISU DOS USUÁRIOS. ****
# TIRAR A POSSIBILIDADE DE CRIAR DUAS VEZES.

db_sample = InventoryManager("central.json")
db_atlas = Mongo_Manager('inventory')
app = Flask(__name__)
# app.secret_key = SECRET_KEY
app.config["JWT_SECRET_KEY"] = "secret"
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('pages/login.html')

@app.route("/validate_user", methods=["POST"])
def validate_user():
    print("Entered")
    email = request.form.get('email')
    # print("user is", email)
    senha = request.form.get('senha').encode('utf-8')
    users_collection = db_atlas.inventory['usuarios']
    user = users_collection.find_one({"Email" : email})
    if user:
        password = base64.b64decode(user["Senha"])
    else:
        password = None
    if password != None and bcrypt.checkpw(senha, password):
        token = create_access_token({"id": str(user["_id"]), "email": user["Email"], "senha" : user["Senha"]})
        resp = make_response(redirect("/"))
        set_access_cookies(resp, token)
        return resp
    else:
        # Retornar o HTML com um campo de coisa inválida.
        return jsonify({"error": "usuario ou senha invalidos"}), 400

@app.route('/', methods=["GET", "POST"])
# @jwt_required()
def index():
    current_user = get_jwt_identity()
    print(current_user)
    colec = db_atlas.inventory.list_collection_names()
    sample = db_sample.get_collection('usuarios')
    if request.method == "POST":
        print("Requisiçao recebida")
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample,  redirect = redirect("/form"))

@app.route('/cadastro/<collection_name>', methods=['POST',  'GET'])
# @jwt_required(locations=["cookies"])
def cadastro(collection_name):
    sample = db_sample.get_collection(collection_name)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    field = db_sample.create_form(collection_name) 
    cat = db_sample.get_collection("categorias")
    print(cat) 
    return render_template('pages/form.html', titulo = "Inicio" , title = collection_name, collection_name = collection_name, field = field, sample = sample, view = sample, date = now, cat = cat )

@app.route('/register', methods=['POST', 'GET'])
def register_user(collection_name = "usuarios"):
    
    # login_check_str = request.args.get('login_check', '{"value": 1 }')

    # try:
    #     login_check = json.loads(login_check_str)
    # except json.JSONDecodeError:
    #     login_check = {"value": 0}

    # print(login_check)  
    # print(type(login_check))  
    # print(login_check)

    # if login_check == None:
    #     login_check = "display : none;"
    
   
    # print(type(login_check))
    login_check = request.args.get('login_check', default=None, type=bool)
   
   
    field = db_sample.create_form(collection_name)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return render_template('pages/register_user.html', field = field, now = now, login_check = login_check)

@app.route('/send_data/<collection_name>', methods= ['POST'])
# @jwt_required()
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}
    if form_values.get("categoria") == "nova_categoria":
        form_values["categoria"] = form_values["nova_categoria"]
        db_sample.save_to_central({'Categoria' : form_values["categoria"]}, "categorias",'create')
        db_sample.insert_into_db('create')
        db_sample.delete_central()
    if form_values.get('nova_categoria') != None:
        del form_values["nova_categoria"]
    print(form_values)
    is_error = None
    if collection_name == "usuarios":
        is_error = None
        sample = db_sample.get_collection("usuarios")
        for x in sample:
            if form_values['Email'] == x["Email"] or form_values['Nome do usuário'] == x["Nome do usuário"]:
                is_error = True
                break  
        if is_error == True:
            login_check = True
            return redirect(url_for('register_user', login_check = login_check))
        InventoryManager.process_user_registration(form_values, collection_name, db_sample)
    db_sample.save_to_central(form_values, collection_name,'create')
    db_sample.insert_into_db('create')
    db_sample.delete_central()
    return redirect('/view/' + collection_name)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
# @jwt_required()
def view(collection_name):
    sample = db_sample.get_collection(collection_name)
    # del sample[0]["Senha"]
    # print(sample)
    if sample:
        
        return render_template('pages/view.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    return jsonify(list(sample))




# form_values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
        # salt = bcrypt.gensalt()
        # password = form_values['Senha'].encode('utf-8')
        # hash_password = bcrypt.hashpw(password, salt)
        # form_values["Senha"] = base64.b64encode(hash_password).decode('utf-8')
        # db_sample.save_to_central(form_values, collection_name,'create')
        # db_sample.insert_into_db('create')
        # db_sample.delete_central()
        # return redirect('/login')