from env import*
import sqlite3

from components.Files_Handler.module.file_handler import Files_Handling

con = sqlite3.connect('C:/Users/Alex_/Work/Área de Trabalho/Repo/inventory/data/teste.sql')
cursor = con.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_name TEXT ,
    contact TEXT,
    email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_name TEXT,
    description TEXT,
    serial_number TEXT,
    focal_point TEXT,
    date TEXT
)
''')

con.commit()

def input_data_db():
    fl = Files_Handling()
    json_data = fl.read_file('central.json', PATTERN_FOLDER)
    try:
        for user in json_data['users']:
            cursor.execute('''
            INSERT INTO users (user_name, contact, email)
            VALUES (?, ?, ?)
            ''', (user['user_name'], user['contact'], user['email']))

        for product in json_data['products']:
            cursor.execute('''
            INSERT INTO products (product_name, description, serial_number, focal_point, date)
            VALUES (?, ?, ?, ?, ?)
            ''', (product['product_name'], product['description'], product['serial_number'], product['focal_point'], product['date']))
        con.commit()
        con.close()

    except sqlite3.Error as e:
        print(f"Erro ao inserir dados nas tabelas: {e}")
        con.close()
        exit(1)