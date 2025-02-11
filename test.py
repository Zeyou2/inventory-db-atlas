from src.inventory_handler import Handle_Operations
from src.connect import Mongo_Manager
import requests

op = Handle_Operations("central.json")
# # print(op.filter_data_struct("usuarios", {'table_visible': 1}))
# hidden = op.filter_data_struct("usuarios", {"form_editable": 'False'})
# hidden = op.field_treatment(hidden)
# print(hidden.values())

logs = op.set_db("logs")
primary_data = op.set_db("primary_data")
operation = op.set_db("operation")

# op.reset_data(primary_data, "categoria")
# op.reset_data(primary_data, "pontos")
# op.reset_data(primary_data, "produtos")
# op.reset_data(primary_data, "usuarios")
op.reset_data(logs, "last_updates")
op.reset_data(operation, "operacao")
op.reset_data(operation,"position")
# op.create_position()
# op.save_log("test")
# print(requests.get("http://localhost:5000/staging/entry").json())

# print(op.dt_struct["produtos"].keys())
