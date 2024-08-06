
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_p import*
import pandas as pd
from components.Files_Handler.module.file_handler import Files_Handling

class Mongo_Manager(Files_Handling):
    def __init__(self, db_name):
        self.client = MongoClient(URI, server_api=ServerApi('1'))
        self.invenctory = self.client[db_name]

    def insert_data(self, entry):
        data = self.read_file('central.json', PATTERN_FOLDER)
        for key, value in data.items():
                docs = self.invenctory[key].insert_many(value.get(entry))
                print(len(docs.inserted_ids))

    def update(self, collection : str, filter_db : dict, new_values : dict):
         result = self.invenctory[collection].update_many(filter_db, {'$set': new_values})
         return result

    def read_docs(self, collection_name):
        db = self.invenctory
        all_docs = []
        # for collection_name in db.list_collection_names():
        collection = db[collection_name]
        docs = collection.find()
        for doc in docs:
            all_docs.append(doc)
        dataframe = pd.DataFrame(all_docs)
        return (all_docs, dataframe)
    
    def close_connection(self):
        try:
            self.client.close()
            print("MongoDB connection closed successfully.")
        except Exception as e:
            print(f'Error closing the connection: {e}')


    def connection_teste(self):
        try:
            self.client.admin.command('ping')
            print("Conectado ao MongoDB Atlas com sucesso!")
        except Exception as e:
            print(f"Erro na conexão: {e}")




# mongo = Mongo_Manager('db_invenctory')
# print(mongo.read_docs())
# def create_data_frame(collection, t):
# data = mongo.read_docs('products')[0]
# # print(data)
# for x in data:
# # x['_id'] = str(x['_id'])
#     # if x['user_name']:
#     dataframe = pd.DataFrame(data)

#         dataframe = pd.DataFrame(data)
