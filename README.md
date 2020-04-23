# Graph CRUD 

A light-weight python library to run CRUD operations on Graph Databases, using JSON inputs.

**Note** Under Active Development. 

```python
from graph_crud.manager import CrudManager

manager = CrudManager("ws://127.0.0.1:8182/gremlin")
msg = {...}
manager.process(msg)
```
### Add Vertex

```json
{
  "type": "vertex",
  "operation_type": "create",
  "data": {
    "label": "Plant",
    "properties":{
      "common_name": "chrysanths",
      "scientific_name": "Chrysanthemum"
    }
  }
}
manager.process(msg)

```

### Add Edge

```json
{
  "type": "Edge",
  "operation_type": "create",
  "data": {
    "label": "BelongsTo",
    "inV": {
      "query":  {
        "type":  "vertex", 
        "operation_type": "find_one", 
        "filter":  {"label":  "Plant", "properties": {"common_name": "chrysanths"} }
      }
    },
    "outV": {"id":  "123-asdv-asd123"},
    "properties":{
      "first_discovered": 1989
    }    
  }
 
}
```
