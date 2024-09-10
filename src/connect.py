
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.utils.env_p import*
import pandas as pd
from src.components.Files_Handler.module.file_handler import Files_Handling

class Mongo_Manager(Files_Handling):
    def __init__(self, db_name):
        self.client = MongoClient(URI, server_api=ServerApi("1"))
        self.inventory = self.client[db_name]

    def teste(self):
        self.inventory["inventory"].insert_many("produtos")

    def insert_into_db(self, operation_type, data = None):
        data = self.read_file("central.json", PATTERN_FOLDER)
        for key, value in data.items():
                docs = self.inventory[key].insert_many(value.get(operation_type))
                print(f'O item foi adicionado!')
        print(f'\nNumero de elementos inseridos no Banco de dados: [{len(docs.inserted_ids)}].')

    def edit_in_db(self, filter_db : dict, operation_type):
        data = self.read_file("central.json", PATTERN_FOLDER)
        for key, value in data.items():
            result = self.inventory[key].update_many(filter_db, {"$set": value.get(operation_type)[0]})
            print(f'O elemento foi atualizado!')
        return result

    def delete_in_db(self, collection_name):
        db = self.inventory
        all_docs = []
        collection = db[collection_name]
        docs = collection.find()
        for doc in docs: 
            all_docs.append(doc)
        
    def get_collection(self, collection_name, filter_by={}, remove_el={'_id': 0}):
        db = self.inventory
        all_docs = []
        collection = db[collection_name]
        docs = collection.find(filter_by, remove_el)
        for doc in docs: 
            all_docs.append(doc)
        return all_docs
    
    def close_connection(self):
        try:
            self.client.close()
            print("MongoDB connection closed successfully.")
        except Exception as e:
            print(f"Error closing the connection: {e}")

    def connection_teste(self):
        try:
            self.client.admin.command("ping")
            print("Conectado ao MongoDB Atlas com sucesso!")
        except Exception as e:
            print(f"Erro na conexão: {e}")


    def reset_inv(self):
        base = {
    "usuarios": {
        "Nome do usuario": "None",
        "Contato": "None",
        "Email": "None",
        "Senha": "None",
        "Registro": "None"
    },
    "produtos": {
        "Nome do produto": "None",
        "Serie": "None",
        "Categoria do Produto": "None",
        "Descrição": "None"
    },
    "transferencia": {
        "data da movimentação": "None",
        "Nome do produto": "None",
        "Quantidade": "None",
        "tipo da transferência do produto": "None",
        "De": "None",
        "Para": "None"
    },
    "pontos": {
        "Nome do local": "None",
        "Tipo": "None"
    }
}
        for key, value in base.items():
                docs = self.inventory[key].insert_many([value])
                print(value)
                print(f'O item foi adicionado!')
        print(f'\nNumero de elementos inseridos no Banco de dados: [{len(docs.inserted_ids)}].')

