from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env_p import *
from connect import Mongo_Manager

class InventoryManager(Mongo_Manager, Files_Handling):
    def __init__(self, base_name):
        Mongo_Manager.__init__(self, "db_invenctory")
        self.base_name = base_name
        self.path = PATTERN_FOLDER
        self.select = self.read_file("estruturas_de_dados.json", self.path)
        self.management = {"Criar":"create", "Editar":"update", "Deletar":"delete"}
        self.method = ["Criar", "Editar", "Deletar"]
        

    @staticmethod
    def get_date():
        while True:
            choose_date = input(f"""
            A data de entrada foi gerada, ({datetime.strftime(datetime.now(), "%d/%m/%Y")}) confirma essa data como data de entrada?
            APERTE "ENTER" SE SIM | ou digite "N" e aperte ENTER se NÃO """)
            if choose_date == "":
                date = datetime.strftime(datetime.now(), "%y%m%d")
                return date
            elif choose_date.lower() == "n":
                day_in = input("\nDigite o dia desejado: ")
                month_in = input("\nDigite o mês desejado: ")
                year_in = input("\nDigite o ano desejado: ")
                date  = datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
                return date
            
    def input_process(self, register, entry):
        result = {}
        structure = self.read_file("estruturas_de_dados.json", self.path)
        get_fields = structure.get(register)
        while True:
            try:
                for key, value in get_fields.items():
                        if "function" in value:
                            func = getattr(self, value[9:])
                            result[key] = func()
                            continue
                        
                        if value == "internal":
                            continue
                        else:
                            result[key] = input(value["pergunta"])
                self.append_file(result, self.base_name, register, entry)

            except KeyboardInterrupt:
                print("\nEncerrando o programa.")
            
            continue_input = input("\nDeseja fazer mais inserções? (s/n): ").strip().lower()
            if continue_input == "n":
                print("Continuando processo...")
                break
            elif continue_input != "s":
                print("\nOpção inválida. Por favor, digite 's' para continuar ou 'n' para sair.")
        
    def delete_json(self):
        data = self.read_file(self.base_name, self.path)
        data = {}
        self.write_file(data, self.base_name, self.path)

    def print_data(self, data, register):
        print("="*78)
        print("-"*30, "[BANCO DE DADOS]", "-"*30)
        print("="*78)
        data = self.read_docs(register)
        print(data[1])
        print("="*78)

    def append_file(self, data, base_name, register, entry):
        try:
            base = self.read_file(self.base_name, self.path)
            base[register][entry].append(data)
        except:
            base[register] = {}
            base[register][entry] = [data]
        self.write_file(base, base_name, self.path)
    
    def menu(self):
        keys = list(dict(self.select).keys())
        print("="*30)
        print("------------[MENU]------------")
        print("="*30)
        for i in range(len(keys)):
            print(f"{i+1}:[{keys[i]}]")
        i = len(keys)+1
        print(f"{i}: Sair")
        print("="*30)
        result = input("\nEscolha a opção desejada: ")
        if int(result) == i:
            return "Saindo do Menu"
        register = keys[int(result)-1]
        try:
            data = self.read_docs(register)
        except Exception:  
            print(f"Ocorreu um erro ao acessar o banco de dados: {register} ")
            r = input(f'"{register}" não existe na base de dados, deseja criá-lo? (s/n) ')
            if r.lower() == 's':
                self.input_process(register, self.management.get(self.method[0]))
                self.insert_data(self.management.get(self.method[0]))
                print("\nA base de dados foi atualizada!")
                self.delete_json()
                print("O cache foi limpo!")
            else:
                print("Registro não foi criado.")
        self.print_data(data, register)
        [print(f"Opção {i + 1}: {self.method[i]}") for i in range(len(self.method))]
        entry = int(input("selecione a opção desejada: "))-1
        if entry == 2:
            self.print_data(data, register)
            rest = data[0][int(input('Selecione o numero do elemento que deseja excluir:  '))]
            result = self.invenctory[register].delete_many(rest)
            print(f"Documentos excluídos: {result.deleted_count}")
            print(self.read_docs(register)[1])
        else:
            if entry == 0:
                self.input_process(register, self.management.get(self.method[entry]))
                self.insert_data(self.management.get(self.method[entry]))
            if entry == 1:
                self.print_data(data, register)
                result = data[0][int(input('Selecione o numero do elemento que deseja mudar:  '))]
                self.input_process(register, self.management.get(self.method[entry]))
                self.update(result, self.management.get(self.method[entry]))
                self.print_data(data, register)
            self.delete_json()
            print("O cache foi limpo!")
        return "Operação concluída! "
       

inv_man = InventoryManager("central.json")
print(inv_man.menu())