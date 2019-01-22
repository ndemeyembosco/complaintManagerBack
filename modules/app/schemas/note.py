from jsonschema import validate
from jsonschema.exceptions import (ValidationError, SchemaError)

note_schema = {
    "type" : "object",
    "properties" : {
        #'_id' : {"type" : "int"},
        "complaint_title" : {"type" : "string"},
        "description": {
            "type":"string"
        },
        "timestamp" : {
            "type": "string",
            "format" : "date-time"
        }

    },
    "required" : ["complaint_title", "description"],
    "additionalProperties": False 
}


def validate_note(data):
    try:
        validate(data, note_schema)
    except ValidationError as e :
        return {'ok': False, 'message': "cannot validate note"}
    except SchemaError as e :
        return {'ok': False, 'message': "schema of note is malformed!"}
    return {'ok': True, 'data' : data}