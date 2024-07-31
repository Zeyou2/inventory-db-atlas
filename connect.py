
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env import*

from components.Files_Handler.module.file_handler import Files_Handling



def connect(URI):
    client = MongoClient(URI, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client


def create_connect(client, db_name):
    db = client[db_name]
    return db

def create_connection_collection(db, col_name):
    return db[col_name]

def insert_data(col, data):
    result = col.insert_many(data)
    n_docs_inserts = len(result.inserted_ids)
    return n_docs_inserts


def remove_item(col):
    item = col.find_one()
    if item is None:
        print("Nenhum documento encontrado.")
        return 0
    
    id_remover = item['_id']
    print(f'ID do item a ser removido: {id_remover}')
    
 
    result = col.delete_one({'_id': id_remover})
    return result.deleted_count
    
#############################client.drop_database('db_inventory') 
# db = client['db_inventory']
# collection = db['products']

# client.list_database_names()
# fl = Files_Handling()
# json_data = fl.read_file('central.json', PATTERN_FOLDER)

# # docs = collection.insert_many(json_data['products'])

# id_remover = collection.find_one()['_id']
# print(id_remover)
# print(collection.delete_one({'_id': id_remover}))


# print(collection.find_one())













# # collection = db['users']







# for key , value in json_data.items():
#     if key == 'users':
#         collection = db['users']
#         collection.insert_one(value[0])
#     if key == 'products':
#         collection = db['products']
#         for dic in value:
#             collection.insert_one(dic)





# con = sqlite3.connect('C:/Users/Alex_/Work/Área de Trabalho/Repo/inventory/data/teste.sql')
# cursor = con.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     user_name TEXT ,
#     contact TEXT,
#     email TEXT
# )
# ''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS products (
#     product_name TEXT,
#     description TEXT,
#     serial_number TEXT,
#     focal_point TEXT,
#     date TEXT
# )
# ''')

# con.commit()

# def input_data_db():
# fl = Files_Handling()
# json_data = fl.read_file('central.json', PATTERN_FOLDER)
# print(json_data['users'])
#     try:
#         for user in json_data['users']:
#             cursor.execute('''
#             INSERT INTO users (user_name, contact, email)
#             VALUES (?, ?, ?)
#             ''', (user['user_name'], user['contact'], user['email']))

#         for product in json_data['products']:
#             cursor.execute('''
#             INSERT INTO products (product_name, description, serial_number, focal_point, date)
#             VALUES (?, ?, ?, ?, ?)
#             ''', (product['product_name'], product['description'], product['serial_number'], product['focal_point'], product['date']))
#         con.commit()
#         con.close()

#     except sqlite3.Error as e:
#         print(f"Erro ao inserir dados nas tabelas: {e}")
#         con.close()
#         exit(1)