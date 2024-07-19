from components.Files_Handler.module.file_handler import Files_Handling
import sqlite3
from datetime import datetime

class inventory:
    def __init__(self, base_name) -> None:
        self.items = {}
        self.base_name = base_name
        self.file_handling = Files_Handling()

    def inventory_create(self):
        data = self.file_handling.read_file('inver.json', pattern_folder= 'D:/@work/inventory/data/')
        for key in data:
            if 'data_de_entrada' == key:
                while True:
                    choose_date = input(f"""
                    A data de entrada foi gerada, ({datetime.strftime(datetime.now(), "%d/%m/%Y")}) confirma essa data como data de entrada?

                    APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO """)
                    if choose_date == '':
                        data[key].append(datetime.strftime(datetime.now(), "%y%m%d"))
                        break
                    elif choose_date.lower() == 'n':
                        day_in = input("\nDigite o dia desejado: ")
                        month_in = input("\nDigite o mês desejado: ")
                        year_in = input("\nDigite o ano desejado: ")
                        data[key]  = datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
                        break
            if 'id' == key:
                data[key].append(int(input('Digite o id do produto que deseja cadastrar. (Apenas numeros!)  \n')))
            if 'descrição' == key:
                data[key].append(input('Descrição do produto. \n'))
            if 'ponto_focal' == key:
                data[key] = {}
            if 'status' == key:
                data[key] = ('disponivel', 'indisponivel')[0]
            if 'serial_number' == key:
                data[key].append(input('Digite o Id do produto que deseja cadastrar. \n'))
        
        self.file_handling.write_file(data, 'inver.json', pattern_folder= 'D:/@work/inventory/data/')
        
            
            # key.append(input('teste'))
       
        # 

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