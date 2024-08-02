
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_p import*
from components.Files_Handler.module.file_handler import Files_Handling

class Mongo_Manager(Files_Handling):
    def __init__(self, db_name):
        self.client = MongoClient(URI, server_api=ServerApi('1'))
        self.invenctory = self.client[db_name]

    def insert_data(self):
        data = self.read_file('central.json', PATTERN_FOLDER)
        for key, value in data.items():
                docs = self.invenctory[key].insert_many(value)
                print(len(docs.inserted_ids))

    def update(self, collection : str, filter_db : dict, new_values : dict):
         result = self.invenctory[collection].update_many(filter_db, {'$set': new_values})
         return result

    def read_docs(self):
        db = self.invenctory
        all_docs = []
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            docs = collection.find()
            for doc in docs:
                all_docs.append(doc)
        return all_docs
    
    def close_connection(self):
        try:
            self.client.close()
            print("MongoDB connection closed successfully.")
        except Exception as e:
            print(f'Error closing the connection: {e}')

# mongo = Mongo_Manager('db_invenctory')
# print(mongo.read_docs())