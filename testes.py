from components.Files_Handler.module.file_handler import Files_Handling
import sqlite3






class inventory:
    def __init__(self, base_name) -> None:
        self.items = {}
        self.base_name = base_name
        self.file_handling = Files_Handling()

    def invenory_create(self):
        
        idd = input('Digite o Id do produto que deseja cadastrar')
        data = self.items[idd] = '2'
       

        self.file_handling.write_file(data, 'inver.json', pattern_folder= 'C:/Users/Alex_/Work/Área de Trabalho/Repo/inventory/')
        pass

    def inventory_read(self):
        pass

    def inventory_update(self):
        pass

    def inventory_delete(self):
        pass



print(inventory('').invenory_create())