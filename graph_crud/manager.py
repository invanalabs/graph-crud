from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from .exceptions import InvalidPayloadException
from .operations.edge import Edge
from .operations.vertex import Vertex


class CrudManager:
    """

    """

    def __init__(self, gremlin_server_url):
        if gremlin_server_url is None:
            raise Exception("Invalid gremlin_server_url. example: ws://127.0.0.1:8182/gremlin")
        self.g = traversal().withRemote(DriverRemoteConnection(gremlin_server_url, 'g'))
        self.vertex = Vertex(self.g)
        # self.edge = Edge(self.g)

    @staticmethod
    def get_type(msg):
        _type = msg.get("type")
        if _type and _type.lower() not in ["vertex", "edge"]:
            raise InvalidPayloadException()
        return _type

    def process(self, msg):
        _type = self.get_type(msg)
        if _type == "vertex":
            return self.vertex.process(msg)
        elif _type == "edge":
            return self.edge.process(msg)
