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

@app.route('resources/{resource_title}/checkout', methods='[POST]')
@require_jwt
def checkout(resource_title):
    # TODO: Get project from request body and update it
    # if resource_title NULL or not a string
    if not resource_title:
        return Response(status=400, response="Malformed request")
    
    # Get our amount from query
    amount = request.args.get('amount')
    
    # Verify We got Amount
    if amount is None:
        return Response(status=400, response="Malformed Request: No amount provided")
    
    # Get our project data and amount checked in
    info = request.args.get('CheckInOutInfo')
    
    if info is None:
        return Response(status=400, response="Malformed Request: No CheckinOutinfo provided")
    
    # Get our project we are checking from
    project = client["projects"].find_one({'title': info["project_title"]})
    
    # Verify that our project has access to this set
    if project["resources"][resource_title] is None:
        return Response(status=403, response="Project has not joined resource")
    
    # Get our resource
    resources = client["resources"]
    resource = resources.find_one({"title": resource_title})

    # Check to see if we have specified resource
    if resource is None:
        return Response(status=404, response="Resource not found")
    
    # If we have enough available to check out 
    if resource["availability"] < amount:
        return Response(status=400, response="Tried to check out too many")
      
    resource["availability"] = resource["availability"] + amount
    project["resources"][resource_title] += amount
    # Update Resource in DB
    client["resources"].update_one({"title": resource_title}, resource)
    client["projects"].update_one({'title': info["project_title"]})
    
    return Response(status=200, response=jsonify(resource), content_type="application/json")

@app.route('resources/{resource_title}/checkin', methods='[POST]')
@require_jwt
def checkin(resource_title):
    # TODO: Get project from request body and update it
    # if resource_title NULL or not a string
    if not resource_title:
        return Response(status=400, response="Malformed request")
    
    # Get our amount from query
    amount = request.args.get('amount')

    # Verify We got Amount
    if amount is None:
        return Response(status=400, response="Malformed Request: No amount provided")
    
    # Get our project data and amount checked in
    info = request.args.get('CheckInOutInfo')
    
    if info is None:
        return Response(status=400, response="Malformed Request: No CheckinOutinfo provided")
    
    # Get our project we are checking from
    project = client["projects"].find_one({'title': info["project_title"]})
    
    # Verify that our project has access to this set
    if project["resources"][resource_title] is None:
        return Response(status=403, response="Project has not joined resource")
    
    # Get our resource
    resources = client["resources"]
    resource = resources.find_one({"title": resource_title})

    # Check to see if we have specified resource
    if resource is None:
        return Response(status=404, response="Resource not found")
    
    # If we are not exceeding capacity TODO: Make this if we are not exceeding the amount specified project has checked in
    if resource["capacity"] < amount + resource["availability"]:
        return Response(status=400, response="Tried to check in too many")
    if project["resources"][resource_title] < amount:
        return Response(status=400, response="Tried to check in too many")
    
    resource["availability"] = resource["availability"] + amount
    project["resources"][resource_title] -= amount
    # Update Resource in DB
    client["resources"].update_one({"title": resource_title}, resource)
    client["projects"].update_one({'title': info["project_title"]})


    
    return Response(status=200, response=jsonify(resource), content_type="application/json")