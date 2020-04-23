from ..exceptions import InvalidConnection
import abc


class OperationsBase(metaclass=abc.ABCMeta):

    def __init__(self, g):
        if g is None:
            raise InvalidConnection()
        self.g = g

    @staticmethod
    def _serialize_vertex_data(data):
        cleaned_data = {}
        for k, v in data.items():
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

    @abc.abstractmethod
    def create(self, data):
        pass

    @abc.abstractmethod
    def update(self, data):
        pass

    @abc.abstractmethod
    def read_one(self, data):
        pass

    @abc.abstractmethod
    def read_many(self, data):
        pass

    @abc.abstractmethod
    def delete(self, data):
        pass

    @abc.abstractmethod
    def validate_data(self, data):
        pass

    def process(self, data):
        # self.validate_data(data)
        operation_type = data.get("operation_type")
        func = getattr(self, operation_type)
        return func(data)
