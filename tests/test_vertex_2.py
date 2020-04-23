from graph_crud.manager import CrudManager

graph_manager = CrudManager("ws://127.0.0.1:8182/gremlin")
#
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
vtx = graph_manager.process(msg)

print("===vtx", vtx)
msg = {
    "type": "vertex",
    "operation_type": "read_one",
    "query": {
        # "label": "Plant", #optional not needed
        "id": 4152
    }
}
vertices = graph_manager.process(msg)

print("===vertex find_one", vertices)
msg = {
    "type": "vertex",
    "operation_type": "read_many",
    "query": {
        "label": "Plant"
    }
}
vertices = graph_manager.process(msg)

print("===vertex read_many", vertices)

msg = {
    "type": "vertex",
    "operation_type": "delete",
    "query": {
        "label": "Plant"
    }
}
vertices = graph_manager.process(msg)
print("===vertex delete", vertices)
