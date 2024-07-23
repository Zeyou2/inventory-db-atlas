from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env import *

class InventoryManager:
    def __init__(self, base_name) -> None:
        self.base_name = base_name
        self.file_handling = Files_Handling()
        self.path = PATTERN_FOLDER

    def inventory_create(self):
        data = self.file_handling.read_file(self.base_name + '.json', self.path)
        for key, value in data.items():
            if '1' == key:
                self.get_date(data[key])
                self.get_id(data[key])
                self.get_description(data[key])
                self.get_focal_point(data[key])
                self.product_status(data[key])
                self.serial_number(data[key])
            if '2' == key:
                self.create_user(data[key])
        self.file_handling.write_file(data, self.base_name + '.json', self.path)


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
        while True:
            try:
                entry['id'] = int(input('Digite o id do produto que deseja cadastrar. (Apenas números!)\n'))
                break
            except ValueError:
                print("\nEntrada inválida. Digite apenas números.")

    def get_description(self, entry):
            entry['description'] = input('Descrição do produto. \n')
    
    def product_status(self, entry):
        tuple_status = ('disponivel', 'indisponivel')
        entry['status'] = tuple_status[0]  

        if "operando" in entry['focal_point']:
            entry['status'] = tuple_status[1]
       

    def get_focal_point(self, entry):
        data = self.file_handling.read_file('local.json', self.path)
        print('LOCAIS: \n')
        for key, value in data.items():
            print(f'* {key} - {value}')
            # selected = input('')
            entry['focal_point'] = key + ' | ' + value
        entry['status'] = self.product_status(entry)

    def serial_number(self, entry):
        entry['serial_number'] = input('Digite o numero de serie do produto. \n')

       
    def create_user(self, entry):
        user = {
        'user_name': input('Digite o nome do usuario a ser cadastrado: \n'),
        'contact': input('Número de contato:  \n'),
        'email': input('E-mail: \n'),
        'permisssions': input('Permissões \n')
        }
        entry['users'].append(user)
    
    def transference_request(self, entry):
        pass
        
      

        

InventoryManager('inventario').inventory_create()