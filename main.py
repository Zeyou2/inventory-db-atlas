from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env import *
import os
class InventoryManager(Files_Handling):
    def __init__(self, base_name) -> None:
        self.base_name = base_name
        self.path = PATTERN_FOLDER

    def get_date(self):
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
                    result[key] = {
                        'name' : input(value['name']['pergunta']),
                        'tipo' : input(value['tipo']['pergunta'])
                        }
                else:
                    result[key] = input(value['pergunta'])
        if key == "date":
                value = self.get_date()
                result[key] = value

        if base.get(register) != None:
            base.get(register).append(result)
        else:
            base[register] = [result]
        self.write_file(base, self.base_name ,self.path)

inv_man = InventoryManager("central.json")
inv_man.input_process("products")
