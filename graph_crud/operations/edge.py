from .base import OperationsBase
from ..exceptions import InvalidVertexException


class Edge(OperationsBase):

    @staticmethod
    def validate_msg(msg):
        required_fields = ["type", "operation_type", "payload"]
        msg_keys = msg.keys()
        for required_field in required_fields:
            if required_field not in msg_keys:
                raise InvalidVertexException("all keys []; are required".format(
                    ",".join(required_fields)
                ))

        payload = msg.get("payload")
        if payload is None or type(payload) is not dict:
            raise InvalidVertexException("Payload need to be dict, Refer documentation.")

        properties = msg.get("payload", {}).get("properties")
        if properties is None or type(properties) is not dict:
            raise InvalidVertexException("properties need to be dict, Refer documentation.")

        required_payload_fields = ["label", "properties"]
        payload_keys = payload.keys()
        for required_field in required_payload_fields:
            if required_field not in payload_keys:
                raise InvalidVertexException("In payload, these keys []; are required".format(
                    ",".join(required_payload_fields)
                ))

    def process(self, msg):
        self.validate_msg(msg)
        operation_type = msg.get("operation_type")
        func = getattr(self, operation_type)
        return func(msg)
