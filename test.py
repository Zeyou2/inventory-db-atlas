from src.inventory_handler import Handle_Operations

op = Handle_Operations("central.json")
# # print(op.filter_data_struct("usuarios", {'table_visible': 1}))
# hidden = op.filter_data_struct("usuarios", {"form_editable": 'False'})
# hidden = op.field_treatment(hidden)
# print(hidden.values())
op.reset_inv("categoria")
op.reset_inv("pontos")
op.reset_inv("produtos")
op.reset_inv("transferência")
op.reset_inv("usuarios")







