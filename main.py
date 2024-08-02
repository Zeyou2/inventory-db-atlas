from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env_p import *
import os
from connect import Mongo_Manager

class InventoryManager(Mongo_Manager, Files_Handling):
    def __init__(self, base_name):
        Mongo_Manager.__init__(self, 'db_invenctory')
        self.base_name = base_name
        self.path = PATTERN_FOLDER

    @staticmethod
    def get_date():
        while True:
            choose_date = input(f"""
            A data de entrada foi gerada, ({datetime.strftime(datetime.now(), "%d/%m/%Y")}) confirma essa data como data de entrada?
            APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO """)
            if choose_date == '':
                date = datetime.strftime(datetime.now(), "%y%m%d")
                return date
            elif choose_date.lower() == 'n':
                day_in = input("\nDigite o dia desejado: ")
                month_in = input("\nDigite o mês desejado: ")
                year_in = input("\nDigite o ano desejado: ")
                date  = datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
                return date
            
    def input_process(self, register):
        result = {}
        structure = self.read_file("estruturas_de_dados.json", self.path)
        get_fields = structure.get(register) 
        for key, value in get_fields.items():
                if "function" in value:
                     func = getattr(self, value[9:])
                     result[key] = func()
                     continue
                
                if value == "internal":
                    continue
                else:
                    result[key] = input(value['pergunta'])

        base = self.read_file(self.base_name, self.path)          
        base[register]['create'].append(result)
        self.write_file(base, self.base_name ,self.path)

    def delete_data(self):
        data = self.read_file(self.base_name, self.path)
        data = {"products": {"create": [], "update":[]},"users": {"create": [],"update":[]}}
        self.write_file(data, self.base_name, self.path)

inv_man = InventoryManager("central.json")
inv_man.input_process('products')
