from .vertex import OperationsBase
import logging
from graph_crud.exceptions import InvalidVertexException

logger = logging.getLogger(__name__)


class Edge(OperationsBase):

    def validate_data(self, query_data):
        pass

    def get_or_create(self, label=None, query=None, inv=None, outv=None):
        # TODO - yet to implement
        pass
        # edg = self.read_one(label=label, query=query, inv=inv, outv=outv)
        # if edg is None:
        #     return self.create(label=label, data=query, inv=inv, outv=outv)
        # return None

    def create(self, label=None, data=None, inv=None, outv=None):
        logger.debug("Creating Edge with label {label} and data {data}".format(
            label=label,
            data=data)
        )
        # TODO - revisit this for performance
        # TODO - get graph object instead of serialised data.
        inv_vtx = self.manager.vertex.read_one(**inv) if "id" in inv \
            else self.manager.vertex.get_or_create(**inv)
        outv_vtx = self.manager.vertex.read_one(**outv) if "id" in outv \
            else self.manager.vertex.get_or_create(**outv)

        inv_vtx_instance = self.manager.g.V(inv_vtx['id'])
        outv_vtx_instance = self.manager.g.V(outv_vtx['id'])
        _ = inv_vtx_instance.addE(label) \
            .to(outv_vtx_instance)
        for property_key, property_value in data.items():
            _.property(property_key, property_value)
        _.next()

    def update(self, id=None, label=None, query=None, data=None):
        logger.debug("Updating vertex with label:id: {label}:{id}:{query}".format(label=label,
                                                                                  id=id,
                                                                                  query=query))
        vtx = self.read_one(id=id, label=label, query=query)
        if vtx:
            _ = self.manager.g.V(vtx['id'])
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
        _ = self.manager.g.V(id) if id else self.manager.g.V()
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

    def read_many(self, label=None, **kwargs):
        pass

    def delete(self, id=None, label=None, **kwargs):
        pass
