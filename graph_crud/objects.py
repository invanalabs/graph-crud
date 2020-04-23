import typesystem


class EdgePayload(typesystem.Schema):
    label = typesystem.String(max_length=100)
    properties = typesystem.Object()
    inV = typesystem.Object()
    outV = typesystem.Object()


class EdgeObject(typesystem.Schema):
    type = typesystem.String(choices=["edge"])
    operation_type = typesystem.String(choices=["create", "update", "read_one", "read_many", "delete"])
    payload = typesystem.Reference(EdgePayload)


class VertexPayload(typesystem.Schema):
    label = typesystem.String(max_length=100)
    properties = typesystem.Object()


class VertexObject(typesystem.Schema):
    type = typesystem.String(choices=["edge"])
    operation_type = typesystem.String(choices=["create", "update", "read_one", "read_many", "delete"])
    payload = typesystem.Reference(VertexPayload)
