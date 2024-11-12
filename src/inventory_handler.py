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
			base = {collection_name: {}}
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
			
	def insert_db_on_form(self, collection, key=""):
		db = self.get_db_by_collection(collection, remove_el={'_id': 0, key: 1})
		return [x[key] for x in db]
	
	def 	field_treatment(self, collection:dict):
	
		for key, value in collection.items():
			value["db_id"] = key
			if value["resp_type"] == "db_list":
				value["resp_type"] = "list"
				[*db_key], [*db_el] = zip(*value["db_origin"].items())
				value["list_elements"] = self.insert_db_on_form(db_key[0], db_el[0])
			value["em_branco"] = "required" if value["em_branco"] == "False" else ""
			value["form_editable"] = "disabled" if value["form_editable"] == "False" else ""
			value["pre_value"] = datetime.strftime(datetime.now(), "%Y-%m-%d") if value["pre_value"] == "datetime_now" else value["pre_value"] 
		return collection


class Handle_Operations(InventoryManager):
	def __init__(self, central):
		super().__init__(central)

	def get_last_code(self, collection_name):
		def parse_code(code: str):
			num_code = code.split("_")[-1]
			try: return (int(num_code))
			except: return None
		num = 0
		db = self.get_db_by_collection(collection_name)
		for elem in db:
			print("elem is: ", elem)
			if (elem.get("codigo") != None):
				num_check = parse_code(elem["codigo"])
				if num_check == None:
					print("ATTENTION - Need to check data obj >> ", elem)
				else:
					num = num_check if num_check > num else num
		return (num + 1)
	
	def make_datapack(self, collection_name, form_visible=0|1):
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
		dados = self.field_treatment(data[collection_name])
		field = list(filter(lambda value: value['form_visible'] == form_visible, dados.values()))

		return field
	
	def filter_data_struct(self, collection_name:str, options:dict):
		t_data = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)[collection_name]
		res_dict = dict()
		def filter_att(filter_db:tuple, options: dict):
			att_true = True
			for key, value in options.items():
				if filter_db[1][key] == value:
					att_true = True
				else:
					att_true = False
					break
			return att_true
		list_process =  list(filter(lambda x: filter_att(x, options), t_data.items()))
		list(map(lambda x: res_dict.update({x[0]:x[1]}), list_process))
		return res_dict

	def make_view_by_att(self, collection_name: str, options:dict):
		t_data = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)[collection_name]
		print(t_data)
		filter_arg = {'_id': 0}
		def non_filtred(filter_db:tuple, options: dict):
			is_hidden = True
			for key, value in options.items():
				if filter_db[1][key] == value:
					is_hidden = False
					break
				else:
					is_hidden = True
			return is_hidden
		pre_filter = list(filter(lambda x: non_filtred(x, options), t_data.items()))
		print(pre_filter)
		list(map(lambda x : filter_arg.update({x[0]:0}), pre_filter))
		return (self.get_db_by_collection(collection_name, remove_el=filter_arg))		

	def process_user_registration(self, form_values):
		sample = self.get_db_by_collection("usuarios")
		for x in sample:
			if form_values['email'] == x["email"] or form_values['nome'] == x["nome"]:
				return None  
		salt = bcrypt.gensalt()
		password = form_values['senha'].encode('utf-8')
		hash_password = bcrypt.hashpw(password, salt)
		
		form_values["senha"] = base64.b64encode(hash_password).decode('utf-8')
		return form_values
		
	def hand_mandatory_data(self, form_value, collection_name):
		hidden = self.filter_data_struct(collection_name, {"form_editable": 'False'})
		hidden = self.field_treatment(hidden)
		for elem in hidden.values():
			for key, value in elem.items():
				if key == "db_id" and value == "codigo":
					form_value[value] = elem["prefixo"] + str(self.get_last_code(collection_name))
				elif key == "db_id" and value == "data_de_registro":
					form_value[value] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
		return form_value

	def process_user_validation(self, form_values):
		"""
	Validates the user based on form input data.

	This method checks if the provided email and password match an existing user 
	in the users database. The user's password stored in the database is encoded 
	in base64 and compared with the encrypted password sent from the form.

	Args:
		form_values (dict): 
			A dictionary containing form values, where 'email' is the user's email 
			and 'senha' is the password provided in the form.

	Returns:
		dict: 
			Returns the user's document as a dictionary if validation is successful.
			Returns `None` if the user is not found or if the password is incorrect.
	"""
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
	
