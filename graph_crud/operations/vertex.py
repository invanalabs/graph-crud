from graph_crud.operations.base import OperationsBase
from graph_crud.exceptions import InvalidVertexException
import logging

logger = logging.getLogger(__name__)


class Vertex(OperationsBase):

    def validate_data(self, query_data):
        required_fields = ["type", "operation_type", "data"]
        query_data_keys = query_data.keys()
        for required_field in required_fields:
            if required_field not in query_data_keys:
                raise InvalidVertexException("all keys []; are required".format(
                    ",".join(required_fields)
                ))

        data = query_data.get("data")
        if data is None or type(data) is not dict:
            raise InvalidVertexException("data need to be dict, Refer documentation.")

        properties = query_data.get("data", {}).get("properties")
        if properties is None or type(properties) is not dict:
            raise InvalidVertexException("properties need to be dict, Refer documentation.")

        required_data_fields = ["label", "properties"]
        data_keys = data.keys()
        for required_field in required_data_fields:
            if required_field not in data_keys:
                raise InvalidVertexException("In data, these keys []; are required".format(
                    ",".join(required_data_fields)
                ))

    def create(self, label=None, data=None):
        logger.debug("Creating vertex with label {label} and data {data}".format(label=label, data=data))
        _ = self.g.addV(label)
        for k, v in data.items():
            _.property(k, v)
        _vtx = _.valueMap(True).next()
        return self._serialize_vertex_data(_vtx)

    def get_or_create(self, label=None, data=None):
        vtx = self.read_one(label=label, data=data)
        if vtx is None:
            return self.create(label=label, data=data)
        return None

    def update(self, id=None, label=None, query=None, data=None):
        logger.debug("Updating vertex with label:id:query {label}:{id}:{query}".format(
            id=id, label=label, query=query))
        vtx = self.read_one(id=id, label=label, query=query)
        data = {} if data is None else data
        if vtx is not None:
            _ = self.g.V(id)
            for k, v in data.items():
                _.property(k, v)
            _vtx = _.valueMap(True).next()
            return self._serialize_vertex_data(_vtx)
        return None

    def filter(self, id=None, label=None, **kwargs):
        """

        :param label:
        :param id:
        :return:
        """
        _ = self.g.V(id) if id else self.g.V()
        if label:
            _.hasLabel(label)
        for k, v in kwargs.items():
            _.has(k, v)
        return _

    def read_one(self, id=None, label=None, **kwargs):
        logger.debug("Finding vertex with label {label} and kwargs {kwargs}".format(label=label, kwargs=kwargs))
        filtered_data = self.filter(id=id, label=label, **kwargs)
        try:
            _ = filtered_data.valueMap(True).next()
            if _:
                return self._serialize_vertex_data(_)
        except Exception as e:
            pass
        return None

    def read_many(self, label=None, **kwargs):
        logger.debug("Updating vertex with label {label} and kwargs {kwargs}".format(label=label, kwargs=kwargs))
        filtered_data = self.filter(label=label, **kwargs)
        cleaned_data = []
        for _ in filtered_data.valueMap(True).toList():
            cleaned_data.append(self._serialize_vertex_data(_))
        return cleaned_data

    def delete(self, id=None, label=None, **kwargs):
        logger.debug("Deleting the vertex with label:id {label}:{id}".format(label=label, id=id))
        filtered_data = self.filter(id=id, label=label, **kwargs)
        filtered_data.drop().iterate()
