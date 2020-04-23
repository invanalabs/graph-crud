import pytest


class TestVertex:
    DATA_CREATE_QUERY = {
        "type": "vertex",
        "operation_type": "create",
        "data": {
            "label": "Plant",
            "properties": {
                "common_name": "chrysanths",
                "scientific_name": "Chrysanthemum"
            }
        }
    }

    UPDATE_QUERY = {
        "type": "vertex",
        "operation_type": "update",
        "data": {
            "label": "Plant",
            "properties": {
                "scientific_name": "Chrysanthemum changed"
            }
        },
        "query": {
            "scientific_name": "Chrysanthemum"
        }
    }

    READ_ONE_QUERY = {
        "type": "vertex",
        "operation_type": "read_one",
        "query": {
            "label": "Plant",  # optional not needed
            "scientific_name": "Chrysanthemum"
        }
    }
    READ_MANY_QUERY = {
        "type": "vertex",
        "operation_type": "read_many",
        "query": {
            "label": "Plant",  # optional not needed
            "scientific_name": "Chrysanthemum"
        }
    }
    DELETE_QUERY = {
        "type": "vertex",
        "operation_type": "delete",
        "query": {
            "label": "Plant",  # optional not needed
            # "scientific_name": "Chrysanthemum"
        }
    }

    @pytest.fixture
    def graph_manager(self):
        from graph_crud.manager import CrudManager
        return CrudManager("ws://127.0.0.1:8182/gremlin")

    def test_create_vertex(self, graph_manager):
        msg = self.DATA_CREATE_QUERY
        vtx = graph_manager.process(msg)

    def test_updated_vertex(self, graph_manager):
        msg = self.UPDATE_QUERY
        vtx = graph_manager.process(msg)

    def test_read_one_vertex(self, graph_manager):
        msg = self.READ_ONE_QUERY
        vtx = graph_manager.process(msg)

    def test_read_vertex(self, graph_manager):
        msg = self.READ_MANY_QUERY
        vtx = graph_manager.process(msg)

    def test_delete_vertex(self, graph_manager):
        msg = self.DELETE_QUERY
        graph_manager.process(msg)
