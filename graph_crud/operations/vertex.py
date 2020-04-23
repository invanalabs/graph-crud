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

    def create(self, query_data):
        logger.debug("Creating vertex with query_data {query_data}".format(query_data=query_data))
        data = query_data.get("data")
        _ = self.g.addV(data['label'])
        for k, v in data['properties'].items():
            _.property(k, v)
        _vtx = _.valueMap(True).next()
        return self._serialize_vertex_data(_vtx)

    def update(self, query_data):
        logger.debug("Updating vertex with query_data {query_data}".format(query_data=query_data))

    def filter(self, query):
        """

        Example Usages:

            msg = {
                    "id": 12344,
                    "label": "Plant" // optional
                }

            msg =  {
                    "label": "Plant",
                    "family": "Asteraceae"
                }


        :param query:
        :return:
        """
        label = query.get("label")
        _id = query.get("id")
        if _id:
            del query['id']
            _ = self.g.V(_id)
        else:
            _ = self.g.V()

        if label:
            del query['label']
            _.hasLabel(label)

        for k, v in query.items():
            _.has(k, v)
        return _

    def read_one(self, query_data):
        logger.debug("Updating vertex with query_data {query_data}".format(query_data=query_data))
        query = query_data.get("query", {})
        filtered_data = self.filter(query)
        try:
            _ = filtered_data.valueMap(True).next()
            if _:
                return self._serialize_vertex_data(_)
        except Exception as e:
            pass
        return None

    def read_many(self, query_data):
        logger.debug("Updating vertex with query_data {query_data}".format(query_data=query_data))
        query = query_data.get("query", {})
        filtered_data = self.filter(query)
        cleaned_data = []
        for _ in filtered_data.valueMap(True).toList():
            cleaned_data.append(self._serialize_vertex_data(_))
        return cleaned_data

    def delete(self, query_data):
        logger.debug("Deleting the vertex with query_data {query_data}".format(query_data=query_data))
        query = query_data.get("query", {})
        filtered_data = self.filter(query)
        filtered_data.drop().iterate()
