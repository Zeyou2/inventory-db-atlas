from flask import Flask, render_template, request, redirect
from env_p import *
from main import InventoryManager

db_sample = InventoryManager("central.json")
select = ["Usuários", 'Produtos']
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    sample = db_sample.read_docs("Usuários")[0]
    if request.method == "POST":
        print(request.data)
    return render_template('teste.html', titulo={'nome': 'teste'}, item_list=sample, redirect = redirect("/form"))

@app.route('/form', methods=["POST","GET"])
def form():
    data = db_sample.read_file('estruturas_de_dados.json', PATTERN_FOLDER) 
    dados = data['Usuários']
    print(dados)
    field = []
    for key, value in dados.items():
        if value['form_visible'] == 1:
            field.append(key)
    return render_template('form.html', field=field)

@app.route('/send_data', methods= ["POST"])
def send(register = None):
    values = {key: value for key, value in request.form.items()}
    db_sample.input_process(register, 'create', values)
    db_sample.insert_data('create')
    db_sample.delete_json()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)