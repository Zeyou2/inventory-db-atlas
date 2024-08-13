from flask import Flask, render_template
from main import *

inv_man = InventoryManager("central.json")

app = Flask(__name__)

@app.route('/')


def menu():

    
    return render_template('teste.html', menu= menu)


if __name__ == '__main__':
    app.run(debug=True)