from flask import Flask, render_template, request, redirect
# from utils.env_p import *
from inventory_handler import InventoryManager
from connect import Mongo_Manager

db_sample = InventoryManager("central.json")
db_atlas = Mongo_Manager('db_invenctory')
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    colec = db_atlas.invenctory.list_collection_names()
    sample = db_sample.read_docs("Usuários")[0]
    if request.method == "POST":
        print(sample)
    return render_template('index.html', titulo = "teste", item_list=colec, redirect = redirect("/form"))

@app.route('/cadastro/usuarios',  methods=['POST', 'GET'] )
def usuarios(register = "Usuários"):
    field = db_sample.create_form(register)
    return render_template('pages/form.html', title = register, field=field)

@app.route('/cadastro/pontos', methods=['POST', 'GET'])
def pontos():
    field = db_sample.create_form("Pontos")
    return render_template('pages/form.html', field=field)

@app.route('/cadastro/produtos', methods=['POST', 'GET'])
def produtos():
    field = db_sample.create_form("Produtos")
    return render_template('pages/form.html', field=field)

@app.route('/send_data', methods= ['POST'])
def send():
    values = {key: value for key, value in request.form.items()}
    db_sample.input_process('Produtos', 'create', values)
    db_sample.insert_data('create')
    db_sample.delete_json()
    return redirect("/")










# @app.route('/cadastro/usuarios', methods=["POST", 'GET'])
# def usuarios():
#     if request.method == 'POST':
#         values = {
#         'name' : request.form['nome'],
#         'contact' : request.form['contato'],
#         'email' : request.form['email'] 
#         }
#         db_sample.input_process('Usuários', 'create', values)
#         db_sample.insert_data('create')
#         db_sample.delete_json()
#         return 'Usuário cadastrado com sucesso!'
#     return render_template('cadastro_usuarios.html')

# @app.route('/cadastro/produtos', methods=["POST", 'GET'])
# def produtos():
#     if request.method == 'POST':
#         values = {
#         'name' : request.form['nome'],
#         'descricao' : request.form['descricao'],
#         'serie' : request.form['serie'],
#         'ponto' : request.form['ponto'], 
         
#         }

#         # 'date' : request.form['date']
#         print(request.form['date'])
#         db_sample.input_process('Produtos', 'create', values)
#         db_sample.insert_data('create')
#         db_sample.delete_json()

#         return 'Produto cadastrado com sucesso!'
#     return render_template('cadastro_produtos.html')

# @app.route('/cadastro/pontos', methods=["POST", 'GET'])
# def pontos():
#     if request.method == 'POST':
#         values = {
#         'name' : request.form['nome'],
#         'tipo' : request.form['tipo'] 
#         }
#         db_sample.input_process('Pontos', 'create', values)
#         db_sample.insert_data('create')
#         db_sample.delete_json()

#         return 'Ponto cadastrado com sucesso!'
#     return render_template('cadastro_pontos.html')



# @app.route('/', methods=["GET", "POST"])
# def main():
#     sample = db_sample.read_docs("Usuários")[0]
#     if request.method == "POST":
#         print(request.data)
#     return render_template('teste.html', titulo={'nome': 'teste'}, item_list=sample, redirect = redirect("/form"))

# @app.route('/form', methods=["POST","GET"])
# def form():
#     data = db_sample.read_file('estruturas_de_dados.json', PATTERN_FOLDER) 
#     dados = data['Usuários']
#     print(dados)
#     field = []
#     for key, value in dados.items():
#         if value['form_visible'] == 1:
#             field.append(key)
#     return render_template('pages/form.html', field=field)

