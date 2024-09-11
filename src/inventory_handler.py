from src.components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from utils.env_p import *
from src.connect import Mongo_Manager
import os

class InventoryManager(Mongo_Manager, Files_Handling):
    def __init__(self, central_data):
        Mongo_Manager.__init__(self, "inventory")
        self.central_data = central_data
        self.path = PATTERN_FOLDER
            
    def save_to_central(self, form_values, collection_name, operation_type):
        try:
            base = self.read_file(self.central_data, self.path)
            base[collection_name][operation_type].append(form_values)
        except:
            base[collection_name] = {}
            base[collection_name][operation_type] = [form_values]
        self.write_file(base, self.central_data, self.path)
            
    def delete_central(self):
        data = self.read_file(self.central_data, self.path)
        data = {}
        self.write_file(data, self.central_data, self.path)

    def create_form(self, collection_name):
        data = self.read_file('estruturas_de_dados.json', PATTERN_FOLDER) 
        dados = data[collection_name]
        field = []
        for key, value in dados.items():
            if value['form_editable'] == 1:
                field.append(value)             
            if key == 'Data de registro':
                field.append(key)
        return field
    
    #Criar aqui uma função para testar o backend das entradas da central.
