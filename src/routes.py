from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies

from utils.env_p import *
from inventory_handler import InventoryManager
from connect import Mongo_Manager
from datetime import datetime


db_sample = InventoryManager("central.json")
db_atlas = Mongo_Manager('inventory')
app = Flask(__name__)

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
    email = request.form.get("email")
    print("user is", email)
    password = request.form.get('senha')
    users_collection = db_atlas.inventory['usuarios']
    user = users_collection.find_one({"Email" : email })
    if user:
        print('entrei')
        token = create_access_token({"id": str(user["_id"]), "email": user["Email"]})
        resp = make_response(redirect("/"))
        set_access_cookies(resp, token)
        return resp
    
    if not(user):
        return jsonify({"error": "usuario nao existe!"}), 400

@app.route('/', methods=["GET", "POST"])
@jwt_required()
def index():
    current_user = get_jwt_identity()
   
    print(current_user)
    colec = db_atlas.inventory.list_collection_names()
    sample = db_sample.get_collection('usuarios')
    if request.method == "POST":
        print("Requisiçao recebida")
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample,  redirect = redirect("/form"))

@app.route('/cadastro/<collection_name>', methods=['POST',  'GET'])
@jwt_required(locations=["cookies"])
def cadastro(collection_name):
    sample = db_sample.get_collection(collection_name)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    field = db_sample.create_form(collection_name)  
    return render_template('pages/form.html', titulo = "Inicio" , title = collection_name, collection_name = collection_name, field = field, sample = sample, view = sample, date = now )

@app.route('/send_data/<collection_name>', methods= ['POST'])
@jwt_required()
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}
    if collection_name == 'usuarios':
        form_values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
    db_sample.save_to_central(form_values, collection_name,'create')
    db_sample.insert_into_db('create')
    db_sample.delete_central()
    return redirect('/view/' + collection_name)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
@jwt_required()
def view(collection_name):
    sample = db_sample.get_collection(collection_name)
    if sample:
        return render_template('pages/view.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    return jsonify(list(sample))

# @app.route('/login', methods=['POST'])
# def login():
    # email = request.json.get('email', None)
    # password = request.json.get('password', None)

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

