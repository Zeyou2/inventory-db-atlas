from components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from env_p import *
from connect import Mongo_Manager

class InventoryManager(Mongo_Manager, Files_Handling):
    def __init__(self, base_name):
        Mongo_Manager.__init__(self, 'db_invenctory')
        self.base_name = base_name
        self.path = PATTERN_FOLDER
        self.select = self.read_file("estruturas_de_dados.json", self.path)
        self.management = {'Criar':"create", 'Editar':"update", 'Deletar':"delete"}
        self.method = ["Criar", "Editar", "Deletar"]

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
                            result[key] = input(value['pergunta'])
                self.append_file(result, self.base_name, register, entry)

            except KeyboardInterrupt:
                print("\nEncerrando o programa.")
            
            continue_input = input("Deseja fazer mais inserções? (s/n): ").strip().lower()
            if continue_input == 'n':
                print("Continuando processo...")
                break
            elif continue_input != 's':
                print("Opção inválida. Por favor, digite 's' para continuar ou 'n' para sair.")


    # def update_data(self, register):
    #     base = self.read_file(self.base_name, self.path)
    #     for entry in base.get(register):
    
    #     print('Executado')
            
# "products": {"create": [], "update":[]},"users": {"create": [],"update":[]}           
    def delete_data(self):
        data = self.read_file(self.base_name, self.path)
        data = {}
        self.write_file(data, self.base_name, self.path)


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
            print(f'{i+1}:[{keys[i]}]')
        i = len(keys)+1
        print(f"{i}: Sair")
        print("="*30)
        result = input("Escolha a opção desejada: ")
        if int(result) == i:
            return "Saindo do Menu"
        t = keys[int(result)-1]
        # self.read_docs(t)[0]
        print(f"O que deseja fazer em {t}")
        [print(f"opção {i + 1}: {self.method[i]}") for i in range(len(self.method))]
        selected = int(input("selecione a opção desejada: "))-1
        # self.input_process(t, self.management.get(self.method[selected]))
        print("arg1 :", t)
        print("arg2 :", self.management.get(self.method[selected]))
        if t == "Usuários":
            for x in range(len(self.management)):
                print(f" {x+1}. {self.management[x]}")
            i = len(keys)+1
            print(f"{i}: Sair")
            print("="*30)
            result = input("Escolha a opção desejada: ")
            if int(result) == i:
                return "Saindo do Menu"
            elif result == '1':
                self.input_process(t, self.management[x-1])

            return result
        return "fim."

inv_man = InventoryManager("central.json")
print(inv_man.menu())





#     def menu(self):
#         while True:
#             print('Menu')
#             print("1. Adicionar dados. ")
#             print("2. Visualizar dados.")
#             print("4. Atualizar/Remover dados")
#             print("6. Sair")

#             choice = input("Escolha uma opção: ")
#             if choice == '1':
#                 self.input_process(self.menu2(), self.management[])
#             elif choice == '2':
#                 self.input_process('users', 'create')
#                 self.insert_data('create')
#                 self.delete_data()
#             elif choice == '3':
#                 self.delete_data()
#             elif choice == '4':
#                 self.update_data('products')
#                 self.edit_data()
#             elif choice == '5':
#                 self.connection_teste()
#             elif choice == '6':
#                 print("Saindo...")
#                 break
#             else:
#                 print("Opção inválida, tente novamente.")
# # print(list(dict(inv_man.select.get(1)).items())[0][0])

# inv_man = InventoryManager("central.json")
# inv_man.insert_data('products')
# print(inv_man.delete_data())

# def me