
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.env_p import*
import pandas as pd
from src.components.Files_Handler.module.file_handler import Files_Handling

class Mongo_Manager(Files_Handling):
    def __init__(self, db_name):
        self.client = MongoClient(URI, server_api=ServerApi("1"))
        self.invenctory = self.client[db_name]

    def insert_data(self, entry):
        data = self.read_file("central.json", PATTERN_FOLDER)
        for key, value in data.items():
                docs = self.invenctory[key].insert_many(value.get(entry))
                print(f'O item foi adicionado!')
        print(f'\nNumero de elementos inseridos no Banco de dados: [{len(docs.inserted_ids)}].')

    def update(self, filter_db : dict, entry):
        data = self.read_file("central.json", PATTERN_FOLDER)
        for key, value in data.items():
            result = self.invenctory[key].update_many(filter_db, {"$set": value.get(entry)[0]})
            print(f'O elemento foi atualizado!')
        return result

    def remove(self, register):
        db = self.invenctory
        all_docs = []
        collection = db[register]
        docs = collection.find()
        for doc in docs: 
            all_docs.append(doc)
        
    def get_collection(self, collection_name, filter_by={}, remove_el={'_id': 0}):
        db = self.invenctory
        all_docs = []
        collection = db[collection_name]
        docs = collection.find(filter_by, remove_el)
        for doc in docs: 
            all_docs.append(doc)
        # dataframe = pd.DataFrame(all_docs)
        # .drop(columns=["_id"])
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


  
    
 