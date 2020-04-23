from .vertex import OperationsBase
import logging
from graph_crud.exceptions import InvalidVertexException

logger = logging.getLogger(__name__)


class Edge(OperationsBase):

    @staticmethod
    def validate_msg(msg):
        pass

    def get_or_create(self):
        pass

    def create(self, label=None, data=None, inv=None, outv=None):
        logger.debug("Creating Edge with label {label} and data {data}".format(label=label,
                                                                               data=data))
        _ = self.g.addE(label)
        for k, v in data.items():
            _.property(k, v)
        _vtx = _.valueMap(True).next()
        return self._serialize_vertex_data(_vtx)

    def update(self, id=None, label=None, query=None, data=None):
        logger.debug("Updating vertex with label:id: {label}:{id}:{query}".format(label=label,
                                                                                  id=id,
                                                                                  query=query))
        vtx = self.read_one(id=id, label=label, query=query)
        print("vtx========", vtx)
        if vtx:
            _ = self.g.V(vtx['id'])
            for k, v in data['properties'].items():
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
        logger.debug("Finding edge with label {label} and kwargs {kwargs}".format(label=label, kwargs=kwargs))
        filtered_data = self.filter(id=id, label=label, **kwargs)
        try:
            _ = filtered_data.valueMap(True).next()
            if _:
                return self._serialize_edge_data(_)
        except Exception as e:
            pass
        return None

    def read_many(self, data):
        pass

    def delete(self, data):
        pass
