from src.inventory_handler import Handle_Operations
from src.connect import Mongo_Manager
import requests
from datetime import datetime, timedelta
op = Handle_Operations("central.json")
# # print(op.filter_data_struct("usuarios", {'table_visible': 1}))
# hidden = op.filter_data_struct("usuarios", {"form_editable": 'False'})
# hidden = op.field_treatment(hidden)
# print(hidden.values())

# logs =  list(filter(lambda x: x["collection"] == "operacao", op.get_db_collection(op.set_db("logs"), "last_updates", {}))).pop()
# print("LOGS: ", logs)
logs = op.set_db("logs")
primary_data = op.set_db("primary_data")
operation = op.set_db("operation")

# changes = operation.get_collection("position").update_many({"codigo_prod":"PROD_1", "id_produto":"123", "posicao":"Agencia"}, update={"$inc":{"quantidade": 1}},upsert=True)
# print("document sent: ", changes.raw_result)
# data = op.get_db_collection(operation, "operacao", {"data_de_registro": {"$gte": logs["timestamp"] + timedelta(seconds=1), "$lte": datetime.now()}})
# print(data)
op.reset_data(primary_data, "categoria")
op.reset_data(primary_data, "pontos")
op.reset_data(primary_data, "produtos")
op.reset_data(primary_data, "usuarios")
op.reset_data(logs, "last_updates")
op.reset_data(operation, "operacao")
op.reset_data(operation,"position")
# op.create_position()
# op.save_log("test")
# print(requests.get("http://localhost:5000/staging/entry").json())

# print(op.dt_struct["produtos"].keys())
