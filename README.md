# Graph CRUD 

A light-weight python library to run CRUD operations on Graph Databases, using JSON inputs.


### Add Vertex

```json
{
  "type": "vertex",
  "operation_type": "create",
  "payload": {
    "label": "Plant",
    "properties":{
      "common_name": "chrysanths",
      "scientific_name": "Chrysanthemum",
      "also_called": ["chrysanths", "mums"]
    }
  }
}
```

### Add Edge

```json
{
  "type": "Edge",
  "operation_type": "create",
  "payload": {
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
