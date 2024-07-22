from components.Files_Handler.module.file_handler import Files_Handling
import sqlite3
from datetime import datetime
from env import *

class InventoryManager:
    def __init__(self, base_name) -> None:
        self.items = {}
        self.base_name = base_name
        self.file_handling = Files_Handling()
        self.path = PATTERN_FOLDER

    def inventory_create(self):
        data = self.file_handling.read_file('inver.json', self.path)
        for key, value in data.items():
            if '1' == key:
                self.get_date(data[key])
                self.get_id(data[key])
                self.get_description(data[key])
                self.get_focal_point(data[key])
                self.product_status(data[key])
                self.serial_number(data[key])
        self.file_handling.write_file(data, 'inver.json', self.path)


    def get_date(self, entry):
            while True:
                choose_date = input(f"""
                A data de entrada foi gerada, ({datetime.strftime(datetime.now(), "%d/%m/%Y")}) confirma essa data como data de entrada?

                APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO """)
                if choose_date == '':
                    entry['entry_date'] = datetime.strftime(datetime.now(), "%y%m%d")
                    break
                elif choose_date.lower() == 'n':
                    day_in = input("\nDigite o dia desejado: ")
                    month_in = input("\nDigite o mês desejado: ")
                    year_in = input("\nDigite o ano desejado: ")
                    entry['entry_date']  = datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
                    break

    def get_id(self, entry):
            entry['id'] = int(input('Digite o id do produto que deseja cadastrar. (Apenas numeros!)  \n'))

    def get_description(self, entry):
            entry['description'] = input('Descrição do produto. \n')

    def get_focal_point(self, entry):
        data = self.file_handling.read_file('local.json', self.path)
        for key, value in data.items():
            entry['focal_point'] = 
            selected = f'''
            LOCAIS: 
            * {key} - {value}

APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO 
'''

    def product_status(self, entry):
            entry['status'] = ('disponivel', 'indisponivel')

    def serial_number(self, entry):
            entry['serial_number'] = input('Digite o numero de serie do produto que deseja cadastrar. \n')
        
    

        
                    
                   
           
        
            
        # key.append(input('teste'))

        # self.items
        # self.items['descrição'] = input('Descrição do produto. ')
        # self.items
        # self.items['status'] = 'disponivel' #tuple('disponivel', 'indisponivel')
        # self.items['serial_number'] = input('Digite o Id do produto que deseja cadastrar')
        # self.file_handling.write_file(self.items, 'inver.json', pattern_folder= 'D:/@work/inventory/data/')
        # self.file_handling.append_file(data, 'inver.json', pattern_folder= 'C:/Users/Alex_/Work/Área de Trabalho/Repo/inventory/')
        # self.items.update('id', )

       
        
        # idd = input('Digite o Id do produto que deseja cadastrar')
        # data = self.items[idd] = '2'
        # pass
    
    # def inventory_read(self):
    #     pass

    # def inventory_update(self):
    #     pass

    # def inventory_delete(self):
    #     pass



inventory('').inventory_create()