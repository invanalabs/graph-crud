from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from .exceptions import InvalidPayloadException
from .operations.edge import Edge
from .operations.vertex import Vertex


class GremlinCRUDManager:
    """

    """

    def __init__(self, gremlin_server_url):
        self.connection = DriverRemoteConnection(gremlin_server_url, 'g')
        if gremlin_server_url is None:
            raise Exception("Invalid gremlin_server_url. example: ws://127.0.0.1:8182/gremlin")
        self.g = traversal().withRemote(self.connection)
        self.vertex = Vertex(self)
        self.edge = Edge(self)

    @staticmethod
    def get_type(_type):
        if _type and _type.lower() not in ["vertex", "edge"]:
            raise InvalidPayloadException()
        return _type

    def process(self, type=None, operation_type=None, payload=None):
        _type = self.get_type(type)
        if _type == "vertex":
            return self.vertex.process(operation_type, **payload)
        elif _type == "edge":
            return self.edge.process(operation_type, **payload)
