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
	
	def	field_treatment(self, collection: dict):
		for key, value in collection.items():
			value["db_id"] = key
			if value["resp_type"] == "db_list":
				value["resp_type"] = "list"
				[*db_key], [*db_el] = zip(*value["db_origin"].items())
				value["list_elements"] = self.insert_db_on_form(db_key[0], db_el[0])
			value["em_branco"] = "required" if value["em_branco"] == "False" else ""
			value["form_editable"] = "readonly" if value["form_editable"] == "False" else ""
			value["pre_value"] = datetime.strftime(datetime.now(), "%Y-%m-%d") if value["pre_value"] == "datetime_now" else value["pre_value"] 
		print("end of field treatment -> dict is: ", collection)
		return collection
class Handle_Operations(InventoryManager):
	def __init__(self, central):
		super().__init__(central)
		self.dt_struct = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)

	def get_last_code(self, collection_name):
		def parse_code(code: str):
			num_code = code.split("_")[-1]
			try: return (int(num_code))
			except: return None
		num = 0
		db = self.get_db_by_collection(collection_name)
		for elem in db:
			# print("elem is: ", elem)
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

		data = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)
		dados = self.field_treatment(data[collection_name])
		# print('dados', dados)
		field = list(filter(lambda value: value['form_visible'] == form_visible, dados.values()))
		# print('field is:', field)
		return field
	
	def filter_data_struct(self, collection_name:str, options:dict):
		t_data = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)[collection_name]
		print("t data is: ",t_data)
		res_dict = {}
    
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
		print("res dict is: ", res_dict)
		return res_dict

	def edit_preview(self, code,  field, collection_name):
		data = self.get_db_by_collection(collection_name, {"codigo": code})[0]
		# print("data in edit preview: ", data)
		# print("field in preview is: ", field)
		for el in field:
			el["pre_value"] = data[el["db_id"]]
		return (field)

	def filter_db_list(self, data: list[dict], options: dict):
		for key, value in options.items():
			# print("key is: ", key ,"and value is: ", value)
			data = list(filter(lambda x: x[key] == value, data))
		return data
	
	def rm_dbfield(self, data: list[dict], remove_list: list):
		for i in remove_list:
			for el in data:
				del el[i]
		return data

	def filter_db_by_dtstruct(self, data: list[dict], collection_name: str, filter_by: dict):
		t_data = self.read_file("estruturas_de_dados.json", PATTERN_FOLDER)[collection_name]
		result = []
		for key, value in filter_by.items():
			t_data = list(filter(lambda x: x[1][key] == value, t_data.items()))
		t_data = list(map(lambda x: x[0], t_data))
		for value in data:
			result.append({x: value[x] for x in t_data})
		return result
		
	def make_view_by_att(self, collection_name: str, filter_els:dict, remove_field = []):
		t_data = self.dt_struct[collection_name]
		remove_status = {'_id': 0}
		sample = (self.get_db_by_collection(collection_name, remove_el=remove_status))
		sample = self.filter_db_list(sample, filter_els)
		sample = self.rm_dbfield(sample, remove_field)
		sample = self.filter_db_by_dtstruct(sample, collection_name, {"table_visible": 1})
		def get_field_name(sample: list[dict], collection:dict):
			# # print("collection is: ", collection)
			final = []
			for el in range(0, len(sample)):
				final.append({})
				for key, value in sample[el].items():
					if collection[key].get("title") != None:
						key_updt = collection[key]["field_name"] + "_title"
					else : key_updt = collection[key]["field_name"]
					final[el].update({key_updt: value})
			return final
		result = get_field_name(sample, t_data)
		return result

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
		form_filtered = self.field_treatment(hidden)
		print("hidden is: ", hidden)
		for elem in form_filtered.values():
			for key, value in elem.items():
				if key == "db_id" and value == "codigo":
					print("Entered in codigo")
					form_value[value] = elem["prefixo"] + str(self.get_last_code(collection_name))
				elif key == "db_id" and value == "data_de_registro":
					form_value[value] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
		form_value["status"] = "enabled"
		print("form value now is:-----------------------------", form_value)
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
		# # print("user is", email)
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

	def make_op_pack(self, data:dict, form_visible=0|1):
		dados = self.field_treatment(data)
		field = list(filter(lambda value: value['form_visible'] == form_visible, dados.values()))

		return field

	def send_treatment(self, collection_name, form_values):
		"""
			Make the procedure to return the correct form_values     
		"""    
		if collection_name == "produtos":
			# Condicional para Seção de Produtos
			if form_values.get("categoria") == "nova_categoria":
				form_values["categoria"] = form_values["nova_categoria"]
				self.save_to_central({'categoria' : form_values["categoria"]}, "categoria",'create')
				self.insert_into_db('create')
				self.delete_central()
			if form_values.get('nova_categoria') != None:
				del form_values["nova_categoria"]

		return form_values
	
	def return_op(self):
		data = self.read_file("transf_op.json", PATTERN_FOLDER)
		operations = data["popular"]["operacoes"]
		return operations
	
	def render_op_form(self, operation:str | None):
		if operation == None:
			return None
		data = self.read_file("transf_op.json", PATTERN_FOLDER)["popular"]
		data = self.make_op_pack(data[operation.lower()], 1)
		all_data = data
		
		list_of_lists = [
			item['list_elements'] for item in data if 'list_elements' in item and not ('db_origin' in item and 'pontos' in item['db_origin'])]
		combined_lists = [" | ".join(items) for items in zip(*list_of_lists)]
		data = list(filter(lambda x : x["db_id"] != "codigo" and x["db_id"] != "nome_produto", data))
		# print(combined_lists)
		return [data, combined_lists, all_data]
	

