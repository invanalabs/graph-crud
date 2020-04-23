from graph_crud.operations.base import OperationsBase
from graph_crud.exceptions import InvalidVertexException
import logging

logger = logging.getLogger(__name__)


class Vertex(OperationsBase):

    def validate_data(self, query_data):
        required_fields = ["type", "operation_type", "payload"]
        query_data_keys = query_data.keys()
        for required_field in required_fields:
            if required_field not in query_data_keys:
                raise InvalidVertexException("all keys []; are required".format(
                    ",".join(required_fields)
                ))

        payload = query_data.get("payload")
        if payload is None or type(payload) is not dict:
            raise InvalidVertexException("Payload need to be dict, Refer documentation.")

        properties = query_data.get("payload", {}).get("properties")
        if properties is None or type(properties) is not dict:
            raise InvalidVertexException("properties need to be dict, Refer documentation.")

        required_payload_fields = ["label", "properties"]
        payload_keys = payload.keys()
        for required_field in required_payload_fields:
            if required_field not in payload_keys:
                raise InvalidVertexException("In payload, these keys []; are required".format(
                    ",".join(required_payload_fields)
                ))

    def create(self, query_data):
        logger.debug("Creating vertex with query_data {query_data}".format(query_data=query_data))
        payload = query_data.get("payload")
        _ = self.g.addV(payload['label'])
        for k, v in payload['properties'].items():
            _.property(k, v)
        _.next()
        return _

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
        _ = filtered_data.valueMap(True).toList()
        if _.__len__() > 0:
            return self._serialize_vertex_data(_[0])
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
