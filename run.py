import sys
import os
from src.connect import Mongo_Manager
from utils.env_p import URI


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.routes import app

if __name__ == '__main__':

     app.run(debug=True, host='0.0.0.0', port=5000)
     # mongo =  Mongo_Manager(URI)
     # db_teste = mongo.set_db("teste_db")
     # print(type(db_teste))
     # # mongo.teste(db_teste, "teste_collection", [{"teste": "teste222"}])
     # #  Mongo_Manager().insert_into_db("teste_db", "create")