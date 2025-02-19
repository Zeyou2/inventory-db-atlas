
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.env_p import URI, PATTERN_FOLDER
import pandas as pd
from src.components.Files_Handler.module.file_handler import Files_Handling


class Mongo_Manager(Files_Handling):
    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi("1"))

    def set_db(self, db_name : str):
        return self.client[db_name]
        
    def teste(self, database, collection_name, data):
        database[collection_name].insert_many(data)
        print(f"Documentos inseridos no DB '{database}', coleção '{collection_name}'!")


    def insert_into_db(self, database: object, collection : str, data:dict|list):
        if type(data) == dict:
            data = [data]
        docs = database[collection].insert_many(data)
        print(f'\nNumero de elementos inseridos no Banco de dados: [{len(docs.inserted_ids)}].')

    def central_add_db(self, database: object, operation_type : str):
        """
        Inserts data into the database from a JSON file.

        This function reads data from a JSON file and inserts items into the database 
        based on the specified operation type.

        Args:
            operation_type (str): The type of operation that determines which set of 
            data will be inserted into the database. This value is used to access 
            the corresponding key in the JSON.

        Returns:
            "teste"
        """
        data = self.read_file("central.json", PATTERN_FOLDER)
        for key, value in data.items():
                docs = database[key].insert_many(value.get(operation_type))
                print(f'O item foi adicionado!')
        print(f'\nNumero de elementos inseridos no Banco de dados: [{len(docs.inserted_ids)}].')

    def edit_db(self, database, collection, filter_db : dict, data, no_exist="insert"):
        upsert = True if no_exist == "insert" else False
        data = [data] if type(data) != list else data
        result = [database[collection].update_many(filter_db, {"$set": ind_data}, upsert=upsert) for ind_data in data]
        print(f'{[i.modified_count for i in result]} elementos foram atualizados!')

    def central_edit_db(self, database, filter_db : dict, operation_type : str, no_exist="insert"):
        """
    Updates documents in the database based on the provided filter.

    This function reads data from a JSON file and updates multiple documents 
    in the database that match the specified filter. The update is based on the 
    operation type specified, which determines the data to be used in the update.

    Args:
        filter_db (dict): A dictionary containing the filter criteria to match the documents 
        in the database that will be updated.
        operation_type (str): The type of operation that defines which set of data 
        will be used to update the documents. This value is used to access the 
        corresponding key in the JSON.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation, including the 
        number of documents matched and modified.
    """
        data = self.read_file("central.json", PATTERN_FOLDER)

        for key, value in data.items():
            if no_exist == "insert":
                result = database[key].update_many(filter_db, {"$set": value.get(operation_type)[0]}, upsert=True)
            else:
                result = database[key].update_many(filter_db, {"$set": value.get(operation_type)[0]})
            print(f'{result.modified_count} elementos foram atualizados!')
        return result
    #verificar função
    def search_in_db(self, database, collection_name):
        all_docs = []
        collection = database[collection_name]
        docs = collection.find()
        for doc in docs: 
            all_docs.append(doc)
        return all_docs
        
    def get_db_collection(self, database, collection_name, filter_by={}, remove_el={'_id': 0}):
        all_docs = []
        print(f"colection name is:", collection_name)
        collection = database.get_collection(collection_name)
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


    def reset_data(self, database, collection):
        database.get_collection(collection).delete_many({})
        resp = {}
        if (collection == "categoria"):
            resp[collection] = {"categoria" : "lorem ipsum"}
        for key, value in resp.items():
                docs = database[key].insert_many([value])
                print(f'O seguinte item foi adicionado!\n', docs.inserted_ids)
    
    def print_db(self, collection):
        db_sample = self.inventory[collection]
        object_db = db_sample.find_one({'Email': 'Alex@mov'}, {"Email" : 1})
        print(object_db)

    

    
