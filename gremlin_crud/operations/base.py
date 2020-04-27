from ..exceptions import InvalidConnection
import abc


class OperationsBase(metaclass=abc.ABCMeta):

    def __init__(self, manager):
        if manager is None:
            raise InvalidConnection()
        self.manager = manager

    @staticmethod
    def _serialize_vertex_data(vtx):
        cleaned_data = {}
        for k, v in vtx.items():
            if str(k) == "T.id":
                if type(v) is dict:
                    cleaned_data['id'] = v.get('@value').strip("#")
                else:
                    cleaned_data['id'] = v
            elif str(k) == "T.label":
                cleaned_data['label'] = v
            else:
                cleaned_data[k] = v[0]
        return cleaned_data

    @staticmethod
    def _serialize_edge_data(data):
        # TODO - implement this later
        return {}

    @abc.abstractmethod
    def create(self, label=None, data=None):
        pass

    @abc.abstractmethod
    def update(self, id=None, label=None, query=None, data=None):
        pass

    @abc.abstractmethod
    def read_one(self, id=None, label=None, **kwargs):
        pass

    @abc.abstractmethod
    def read_many(self, label=None, **kwargs):
        pass

    @abc.abstractmethod
    def delete(self, id=None, label=None, **kwargs):
        pass

    @abc.abstractmethod
    def validate_data(self, data):
        pass

    @abc.abstractmethod
    def get_or_create(self, label=None, data=None):
        pass

    def process(self, operation_type=None, **kwargs):
        # self.validate_data(data)
        func = getattr(self, operation_type)
        return func(**kwargs)
