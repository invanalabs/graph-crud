from graph_crud.manager import CrudManager

manager = CrudManager("ws://127.0.0.1:8182/gremlin")

msg = {
    "type": "vertex",
    "operation_type": "create",
    "payload": {
        "label": "Plant",
        "properties": {
            "common_name": "chrysanths",
            "scientific_name": "Chrysanthemum"
        }
    }
}
manager.process(msg)
