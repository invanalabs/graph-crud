import pytest


class TestVertex:

    @pytest.fixture
    def graph_manager(self):
        from graph_crud.manager import CrudManager
        return CrudManager("ws://127.0.0.1:8182/gremlin")

    def test_create_vertex(self, graph_manager):
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

    def test_delete_vertex(self, graph_manager):
        msg = {
            "type": "vertex",
            "operation_type": "delete",
            "query": {
                "id": 8248
            }
        }
        graph_manager.process(msg)
