from src.inventory_handler import Handle_Operations

op = Handle_Operations("central.json")
print(op.put_required_elem("produtos", "Nome do produto"))