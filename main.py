from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env import *
import os
class InventoryManager(Files_Handling):
    def __init__(self, base_name) -> None:
        self.base_name = base_name
        self.path = PATTERN_FOLDER

    def inventory_create(self):
        data = self.read_file(self.base_name, self.path)
        for key in data:
                    # self.get_product_description_sr(data[key])
                    self.get_focal_point(data[key])
                    self.product_status(data[key])
                    self.get_date(data[key]) 
        self.write_file(data, self.base_name + '.json', self.path)

    # def get_product_description_sr(self, entry):
    #     entry['description'] = input('Descrição do produto: \n')
    #     entry['product_name'] = input('Nome do produto. \n')
    #     entry['serial_number'] = input('Digite o numero de serie do produto: \n')

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

    def product_status(self, entry):
        tuple_status = ('disponível', 'não disponível')
        entry['status'] = tuple_status[1]  

        if entry['focal_point']['tipo'] == "armazenamento":
            entry['status'] = tuple_status[0]
       
    # def get_focal_point(self, entry):
    #     data = self.read_file('local.json', self.path)
    #     for key in data:
    #         entry['focal_point'] = data[key]
    #         break
    #     self.product_status(entry)

    def add_local(self):
        data = self.read_file('local.json', self.path)
        for key, value in data.items():
            if key == '2':
                value['nome'] = input('local name: ')
                value['tipo'] = input('local desc: ')
                break
        self.write_file(data, 'local.json', self.path)

    def transference_request(self):
        data = self.read_file('inventario.json', self.path)
        for key, value in data.items():
            if 'disponível' in value.get('status', '' ):
                    self.add_local()
    
    def create_user(self):
        data = self.read_file('users.json', self.path)
        user = {
        'user_name': input('Digite o nome do usuario a ser cadastrado: \n'),
        'contact': input('Número de contato:  \n'),
        'email': input('E-mail: \n'),
        'permisssions': input('Permissões: \n')
        }
        data['users'].append(user)
        self.write_file(data, 'users.json', self.path)
# InventoryManager('inventario').transference_request()

    def input_process(self, register):
        if os.path.exists(self.path + "/" + self.base_name):
            base = self.read_file(self.base_name, self.path)
        else:
            base = {}
        result = {}
        structure = self.read_file("estruturas_de_dados.json", self.path)
        get_fields = structure[register]
        for key, value in get_fields.items():
        
            if value == "internal":
                continue
            if key == 'focal_point':
               result[key] = input(value['name']['pergunta'])
               result[key] = input(value['tipo']['pergunta'])
            else:
                result[key] = input(value['pergunta'])
        print(base)
        print('result is:', result)
        if base.get(register) != None:
            print("passed on first")
            base.get(register).append(result)
        else:
            base[register] = [result]
        print("base is? ", base)
        # self.inventory_create()
        self.write_file(base, self.base_name ,self.path)
inv_man = InventoryManager("central.json")
inv_man.input_process("products")