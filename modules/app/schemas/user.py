from jsonschema import validate
from jsonschema.exceptions import ValidationError 
from jsonschema.exceptions import SchemaError 

user_schema = {
    "type" : "object",
    "properties" : {
        "user_id" : {"type" : "number"},
        "name" : {"type" : "string"},
        "email": {
            "type":"string"
            , "format" : "email"
        },
        "password" : {
            "type": "string",
            "minLength" : 6
        }

    },
    "required" : ["email", "password"],
    "additionalProperties": False 
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': "This is the error"}
    return {'ok': True, 'data': data }

    