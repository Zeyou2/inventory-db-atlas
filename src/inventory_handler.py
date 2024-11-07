from src.components.Files_Handler.module.file_handler import Files_Handling
from datetime import datetime
from utils.env_p import PATTERN_FOLDER
from src.connect import Mongo_Manager
import bcrypt
import base64

class InventoryManager(Mongo_Manager, Files_Handling):
    def __init__(self, central_data):
        """
        Manages inventory operations by handling data storage and retrieval.

        This class integrates functionalities from MongoDB and file handling 
        to manage inventory data. It provides methods for saving form data 
        to a central structure, deleting all central data, and creating forms 
        based on editable fields from specified collections.

        Attributes:
            central_data (str): The path to the central data file.
            path (str): The directory path for file operations.
        """
        Mongo_Manager.__init__(self, "inventory")
        self.central_data = central_data
        self.path = PATTERN_FOLDER
            
    def save_to_central(self, form_values, collection_name, operation_type):
        """
    Saves form values to a central data structure in a specified collection.

    This function attempts to read existing data from a central file and append 
    the provided form values to the appropriate collection and operation type. 
    If the collection or operation type does not exist, it creates them.

    Args:
        form_values (dict): The values from the form to be saved in the central data.
        collection_name (str): The name of the collection where the data will be saved.
        operation_type (str): The type of operation that specifies the category 
            under which the form values will be stored.

    Returns:
        None
    """
        try:
            base = self.read_file(self.central_data, self.path)
            base[collection_name][operation_type].append(form_values)
        except:
            base[collection_name] = {}
            base[collection_name][operation_type] = [form_values]
        self.write_file(base, self.central_data, self.path)
            
    def delete_central(self):
        """
    Deletes all data from the central data structure.

    This function reads the current data from the central file and 
    resets it to an empty dictionary, effectively deleting all stored data. 
    It then writes the empty dictionary back to the file.

    Returns:
        None
    """
        data = self.read_file(self.central_data, self.path)
        data = {}
        self.write_file(data, self.central_data, self.path)

    def create_form(self, collection_name):
        """
    Creates a form structure based on editable fields from a specified collection.

    This function reads data from a JSON file and retrieves the fields 
    from the specified collection that are marked as editable. 
    It compiles these fields into a list for form creation.

    Args:
        collection_name (str): The name of the collection from which to retrieve 
        editable fields for the form.

    Returns:
        list: A list of fields that are editable and can be used to create a form.
    """
        data = self.read_file('estruturas_de_dados.json', PATTERN_FOLDER) 
        dados = data[collection_name]
        field = []
        for key, value in dados.items():
            if value['form_editable'] == 1:
                field.append(value)                    
        return field
    
class Handle_Operations(InventoryManager):
    def __init__(self, central):
        super().__init__(central)
        
    def process_user_registration(self, form_values):
        sample = self.get_collection("usuarios")
        for x in sample:
            if form_values['Email'] == x["Email"] or form_values['Nome do usuário'] == x["Nome do usuário"]:
                return None  
        form_values["Registro"] = datetime.strftime(datetime.now(), "%Y-%m-%d")
        salt = bcrypt.gensalt()
        password = form_values['Senha'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, salt)
        
        form_values["Senha"] = base64.b64encode(hash_password).decode('utf-8')
        return form_values
    
    def process_user_validation(self, form_values):
        email = form_values.get('email')
        # print("user is", email)
        senha = form_values.get('senha').encode('utf-8')
        users_collection = self.inventory['usuarios']
        user = users_collection.find_one({"Email" : email})
        if user:
            password = base64.b64decode(user["Senha"])
        else:
            password = None
        if password != None and bcrypt.checkpw(senha, password):
            return user
        else:
            return None

    def send_treatment(self, collection_name, form_values):
        """
            Make the procedure to return the correct form_values     
        """    
        if collection_name == "produtos":
            # Condicional para Seção de Produtos
            if form_values.get("categoria") == "nova_categoria":
                form_values["categoria"] = form_values["nova_categoria"]
                self.save_to_central({'Categoria' : form_values["categoria"]}, "categorias",'create')
                self.insert_into_db('create')
                self.delete_central()
            if form_values.get('nova_categoria') != None:
                del form_values["nova_categoria"]
        return form_values
    
    