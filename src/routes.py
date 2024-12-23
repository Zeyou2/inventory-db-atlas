from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from utils.env_p import *
from inventory_handler import Handle_Operations
from datetime import datetime
from bson.objectid import ObjectId



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
    # print("Entered")
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
    # print('field is:', field)
   
    return render_template('pages/register_user.html', field = field, now = now, login_check = login_check)

@app.route('/send_data/<collection_name>', methods= ['POST'])
# @jwt_required()
def send(collection_name):
    form_values = {key: value for key, value in request.form.items()}

    # print('teste >>>>>>>', form_values)
    url_args = request.args.to_dict()
    # print("form values before: ", form_values)
    if url_args.get('op_type') != None:
        redirect_to = "/operation"
        form_values.update({'operacao': url_args.get("op_type")})
    else:
        redirect_to = "/view/" + collection_name

    if collection_name != "transferencia":
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
    return redirect(redirect_to)

@app.route('/view/<collection_name>', methods=['POST', 'GET'])
# @jwt_required()
def view(collection_name):
    sample = manage_op.make_view_by_att(collection_name, {"status": "enabled"}) 

    return render_template('pages/view.html', titulo = "Inicio", collection_name = collection_name, sample = sample )
    # return jsonify(list(sample))

@app.route('/operation', methods=['POST',  'GET'])
# @jwt_required(locations=["cookies"])
def operation():
    options = manage_op.return_op()
    op_type = request.args.get("op_type")
    field = manage_op.render_op_form(op_type)
    final_field, combined_lists = list(), list()
    
    if op_type != None:
        combined_lists = field[1]
        final_field = field[0]
    return render_template('pages/populate.html', options=options, op_type=op_type, field=final_field, combined_lists = combined_lists)

@app.route('/edit_card/<collection_name>/<codigo>', methods=['POST', 'GET'])
# @jwt_required(locations=["cookies"])
def edit_card(collection_name, codigo):
    field = manage_op.make_datapack(collection_name, 1)
    field = manage_op.edit_preview(codigo, field, collection_name)
    # sample = manage_op.make_view_by_att(collection_name, {}, ty = "edit")
    return render_template('pages/edit_form.html', codigo = codigo, title = collection_name, collection_name = collection_name, field = field)


@app.route('/send/edit/<collection_name>/<codigo>', methods = ["POST", "GET"])
# @jwt_required(locations=["cookies"])
def edit(collection_name, codigo):
    form_values = {key: value for key, value in request.form.items()}
    # form_values['data_de_registro'] = 'edit_in ' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    form_values = manage_op.hand_mandatory_data(form_values, collection_name)
    form_values = manage_op.send_treatment(collection_name, form_values)
    resultado = manage_op.inventory[collection_name].update_one({'codigo' : codigo}, {'$set': form_values})
    # print(f"Documentos modificados: {resultado.modified_count}")
    # print("form", collection_name, codigo, form_values)
    return redirect('/view/' + collection_name)

@app.route('/disable_card/<collection_name>/<codigo>', methods=['POST', 'GET'])
# @jwt_required(locations=["cookies"])
def disable_card(collection_name, codigo):
    resultado = manage_op.inventory[collection_name].update_one({"codigo":codigo} ,  {'$set': {"status" : 'disabled'}})
    # print(f"Documentos modificados: {resultado.modified_count}")
    return redirect('/view/'+ collection_name)