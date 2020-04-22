from ..exceptions import InvalidConnection


class OperationsBase:

    def __init__(self, g):
        if g is None:
            raise InvalidConnection()
        self.g = g
