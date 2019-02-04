import json
from flask import make_response
from flask import Flask, Response, abort

JSON_MIME_TYPE = 'application/json'

def success_(data):
    return data, 200, {'Content-Type': JSON_MIME_TYPE}

def success_json(data):
    content = json.dumps(data)
    return content, 200, {'Content-Type': JSON_MIME_TYPE}

def success_response(data):
    response = Response(
        json.dumps(data), status=200, mimetype=JSON_MIME_TYPE
    )
    return response 