from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from utils.env_p import *
from connect import Mongo_Manager
from inventory_handler import Handle_Operations
from datetime import datetime



manage_op = Handle_Operations("central.json")
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
    form_values = request.form
    user = manage_op.process_user_validation(form_values)
    if user == None:
        return jsonify({"error": "usuario ou senha invalidos"}), 400
    else: 
        token = create_access_token({"id": str(user["_id"]), "email": user["Email"], "senha" : user["Senha"]})
        resp = make_response(redirect("/"))
        set_access_cookies(resp, token)
        return resp        

@app.route('/', methods=["GET", "POST"])
# @jwt_required()
def index():
    # current_user = get_jwt_identity()
    # print(current_user)

    colec = manage_op.inventory.list_collection_names()
    sample = manage_op.get_db_by_collection('usuarios')
    if request.method == "POST":
        print("Requisiçao recebida")
    return render_template('index.html', titulo = "Inicio", item_list = colec, sample = sample,  redirect = redirect("/form"))

@app.route('/cadastro/<collection_name>', methods=['POST',  'GET'])
# @jwt_required(locations=["cookies"])
def cadastro(collection_name):
    field = manage_op.make_datapack(collection_name, 1) 
    
    return render_template('pages/form.html', titulo = "Inicio" , title = collection_name, collection_name = collection_name, field = field)

@app.route('/register', methods=['POST', 'GET'])
def register_user(collection_name = "usuarios"):
    login_check = request.args.get('login_check', default=None, type=bool)
    field = manage_op.make_datapack(collection_name, 1)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d")
    return render_template('pages/register_user.html', field = field[0], now = now, login_check = login_check)

@app.route('/send_data/<collection_name>', methods= ['POST'])
# @jwt_required()
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}
    form_values = manage_op.hand_mandatory_data(form_values, collection_name)
    form_values = manage_op.send_treatment(collection_name, form_values)
    # print("prestes a enviar -> form values is: ", form_values)
    if collection_name == "usuarios":
        form_values = manage_op.process_user_registration(form_values)
        if form_values == None:
            return redirect(url_for('register_user', login_check = True))
    
    manage_op.save_to_central(form_values, collection_name,'create')
    manage_op.insert_into_db('create')
    manage_op.delete_central()
    return redirect('/view/' + collection_name)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
# @jwt_required()
def view(collection_name):
    codigo = 'prod_2'
    sample = manage_op.make_view_by_att(collection_name, {'table_visible': 1})
    for x in sample:
        if x['Código'] == codigo:
            print('entrei')
            teste = manage_op.get_db_by_collection(collection_name, {'codigo' : codigo}, {'id'})


    print("------------------------------------\n",teste)
    if sample:
        return render_template('pages/view.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    return jsonify(list(sample))

@app.route('/operacao', methods=['POST',  'GET'])
# @jwt_required(locations=["cookies"])
def operation(op_type=""):
    options = manage_op.return_op()
    op_type = None if request.args.get("op_type") == None else request.args.get("op_type")
    field = manage_op.render_op_form(op_type)
    # print("op type is: ", op_type)
    # print("field is: ", field)
    return render_template('pages/populate.html', titulo = "Inicio", options=options, op_type=op_type, field=field)









@app.route('/edit/<collection_name>/<codigo>', methods=['POST', 'GET'])
# @jwt_required(locations=["cookies"])
def edit_card(collection_name, codigo):
    sample = manage_op.make_view_by_att(collection_name, {'table_visible': 1})
    for x in sample:
        if x['Código'] == codigo:
            print('entrei')
            teste = manage_op.get_db_by_collection(collection_name, {'codigo' : codigo}, {'id'})
    return render_template()











# Rota de testes para visulização de cards
@app.route('/view_test/<collection_name>', methods=['POST', 'GET'])
# @jwt_required()
def view_teste(collection_name):
    print("view test - collection: ", collection_name)
    sample = manage_op.make_view_by_att(collection_name, {'table_visible': 1})
    print("------------------------------------\n",sample)
    if sample:
        return render_template('pages/view_test.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    return jsonify(list(sample))

@app.route('/div', methods=['POST',  'GET'])
# @jwt_required(locations=["cookies"])
def div_teste():
    
    return render_template('pages/div_teste.html')