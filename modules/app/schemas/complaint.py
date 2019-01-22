from jsonschema import validate
from jsonschema.exceptions import (ValidationError, SchemaError)

complaint_schema = {
    "type": "object",
    "properties" : {
        "title" : {
            "type" : "string"
        },
        "creator_name" : {
            "type": "string"
        },
        "assigned_to" : {
            "type" : "string"
        },
        "creator_email" : {
            "type" : "string",
            "format" : "email"
        },
        "status" : {
            "type" : "string",
            "enum" : ["opened", "unopened", "pending", "solved"]
        },
        "about_brand" : {
            "type" : "string",
            "enum" : ["volvo", "subaru", "cadillac"]
        },
        "telephone" : {
            "type" : "string",
            "format" : "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
        },
        "timestamp" : {
            "type" : "string",
            "format" : "date-time"
        },
        "model" : {
            "type" : "string"
        },
        "description" : {
            "type" : "string"
        }
    },
    "required" : ["creator_name"
                  , "creator_email"
                  , "status"
                  , "about_brand"
                  , "telephone"
                  , "description"
                  , "title"
                 ],
    "additionalProperties" : False 
}

complaint_update_schema = {
    "type" : "object",
    "properties" : {
        "id" : {"type" : "string"},
        "payload" : {
            "type" : "object",
            "properties" : {
                "title" : {
                    "type" : "string"
                },
                "description" : {
                    "type" : "string"
                },
                "status" : {
                    "type" : "string",
                    "enum" : ["volvo", "subaru", "cadillac"]
                },
                "creator_name" : {
                    "type" : "string"
                },
                "assigned_to" : {
                    "type" : "string"
                },
                "creator_email" : {
                    "type" : "string",
                    "format" : "email"
                },
                "status" : {
                    "type" : "string",
                    "enum" : ["opened", "unopened", "pending", "solved"]
                },
                "about_brand" : {
                    "type" : "string",
                    "enum" : ["volvo", "subaru", "cadillac"]
                },
                "telephone" : {
                    "type" : "string",
                    # "format" : "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
                },
                "date-created" : {
                    "type" : "string",
                    "format" : "date-time"
                },
                "model" : {
                    "type" : "string"
                }
            },
            "additionalProperties" : False 
        }
    },
    "required" : ["creator_name", "creator_email", "status", "about_brand", "telephone", "description"],
    "additionalProperties" : False 
}


def validate_complaint(data):
    try:
        validate(data, complaint_schema)
    except ValidationError as e :
        return {'ok': False, 'message': "cannot validate complaint"}
    except SchemaError as e :
        return {'ok': False, 'message': "schema of complaint is malformed!"}
    return {'ok': True, 'data' : data}


def validate_complaint_update(data):
    try:
        validate(data, complaint_update_schema)
    except ValidationError as e :
        return {'ok': False, 'message': e}
    except SchemaError as e :
        return {'ok': False, 'message': e}
    return {'ok': True, 'data' : data}