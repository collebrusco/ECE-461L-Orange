import time
from flask import make_response, request, Response, jsonify
from app import app, client, mongo_authdb

from .auth import check_hash, encode, require_jwt, get_hash, User


@app.route('resources', methods=['GET'])
@require_jwt
def all_resources():
    

    # grab resources from table
    resources = client["resources"]

    return Response(status=200, response=resources, content_type="application/json")

@app.route('resources/{resource_id}/checkout', methods='[POST]')
@require_jwt
def checkout(resource_id):
    # TODO: Get user from jwt and put our resource into their project
    # if resource_id NULL or not a string
    if not resource_id:
        return Response(status=400, response="Malformed request")
    
    # Get our amount from query
    amount = request.args.get('amount')
    
    # Verify We got Amount
    if amount is None:
        return Response(status=400, response="Malformed Request: No amount provided")
    
    # Get our resource
    resources = client["resources"]
    resource = resources.find_one({"id": resource_id})

    if resource is None:
        return Response(status=404, response="Resource not found")
    
    if resource["availability"] < amount:
        return Response(status=400, response="Tried to check out too many")
    else:
        resource["availability"] = resource["availability"] - amount
        client["resources"].update_one({"id": resource_id}, resource)
    
    return Response(status=200, response=jsonify(resource), content_type="application/json")

@app.route('resources/{resource_id}/checkin', methods='[POST]')
@require_jwt
def checkin(resource_id):
    # TODO: Get user from jwt and put our resource into their project
    # if resource_id NULL or not a string
    if not resource_id:
        return Response(status=400, response="Malformed request")
    
    # Get our amount from query
    amount = request.args.get('amount')
    
    # Verify We got Amount
    if amount is None:
        return Response(status=400, response="Malformed Request: No amount provided")
    
    # Get our resource
    resources = client["resources"]
    resource = resources.find_one({"id": resource_id})

    if resource is None:
        return Response(status=404, response="Resource not found")
    
    if resource["capacity"] < amount + resource["availability"]:
        return Response(status=400, response="Tried to check in too many")
    else:
        resource["availability"] = resource["availability"] + amount
        client["resources"].update_one({"id": resource_id}, resource)
    
    return Response(status=200, response=jsonify(resource), content_type="application/json")