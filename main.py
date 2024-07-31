from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env import *
import os

class InventoryManager(Files_Handling):
    def __init__(self, base_name) -> None:
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
        base = {}
        result = {}
        structure = self.read_file("estruturas_de_dados.json", self.path)
        get_fields = structure[register] 
        for key, value in get_fields.items():
                if "function" in value:
                     func = getattr(self, value[9:])
                     result[key] = func()
                     continue
                
                if value == "internal":
                    continue
                else:
                    result[key] = input(value['pergunta'])
                    
        if base.get(register) != None:
            base.get(register).append(result)
        else:
            base[register] = [result]
        self.write_file(base, self.base_name ,self.path)

    def check_focal_point(self, focal_point_name):
        data = self.read_file(self.path + "/" + self.base_name)
        if 'focal_point' in data:
            for entry in data['focal_point']:
                rest = entry.get("name")
                if rest == focal_point_name:
                    return rest
                else:
                    print('Esse ponto ainda não foi criado, deseja criá-lo?')



inv_man = InventoryManager.get_date()
inv_man.input_process("products")

