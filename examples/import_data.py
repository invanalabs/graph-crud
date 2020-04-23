from graph_crud.manager import CrudManager
import copy

graph_manager = CrudManager("ws://127.0.0.1:8182/gremlin")

nodes = [
    {
        "name": "Bamboo Orchid",
        "other_name": "Arundina Graminifolia",
        "image_url": "https://themysteriousworld.com/wp-content/uploads/2019/09/Bamboo-Orchid.webp",
        "found_in": ["India", "Sri Lanka", "China", "Singapore", "Common Country"],
        "__metadata__": {
            "label": "Orchid",
            "__mapping__": {
                "found_in": {"label": "Country", "field_name": "name"}
            }
        }
    },
    {
        "name": "Spathoglottis Plicata",
        "other_name": "Philippine ground orchid",
        "image_url": "https://themysteriousworld.com/wp-content/uploads/2019/09/Spathoglottis-Plicata.webp",
        "found_in": ["Asia", "Australia", "western Pacific regions", "Common Country"],
        "__metadata__": {
            "label": "Orchid",
            "__mapping__": {
                "found_in": {"label": "Country", "field_name": "name"}
            }
        }
    },
    {
        "name": "Miltassia",
        "image_url": "https://themysteriousworld.com/wp-content/uploads/2019/09/Miltassia.webp",
        "__metadata__": {
            "label": "Orchid"
        }
    },
]


def delete_orchids_data():
    delete_orchids_query = {
        "type": "vertex",
        "operation_type": "delete",
        "payload": {
            "label": "Orchid",
        }
    }
    graph_manager.process(**delete_orchids_query)
    delete_orchids_query = {
        "type": "vertex",
        "operation_type": "delete",
        "payload": {
            "label": "Country",
        }
    }
    graph_manager.process(**delete_orchids_query)


delete_orchids_data()


def get_or_create(label=None, data=None):
    query = {
        "type": "vertex",
        "operation_type": "get_or_create",
        "payload": {"label": label, "query": data},
    }

    return graph_manager.process(**query)


def create_edge(label=None, properties=None, inv=None, outv=None):
    return graph_manager.process(
        type="edge",
        operation_type="create",
        payload={
            "label": label,
            "data": properties,
            "inv": inv,
            "outv": outv
        }
    )


for node in nodes:
    node_backup = copy.deepcopy(node)
    node_metadata = node_backup.get("__metadata__", {})
    mapping_keys = node_metadata.get("__mapping__", {}).keys()
    for key in mapping_keys:  # delete the mapping fields, which are lists,
        del node[key]
    if "__metadata__" in node:  # delete __mapping__ data,
        del node['__metadata__']
    vtx = get_or_create(label=node_metadata["label"], data=node)
    for field_name, field_mapping in node_metadata.get("__mapping__", {}).items():
        field_data = node_backup[field_name]
        for field_datum in field_data:
            edg = create_edge(
                label=field_name,
                properties={},
                inv={"id": vtx['id']},
                outv={
                    "label": field_mapping['label'],
                    "query": {field_mapping['field_name']: field_datum}
                }
            )
