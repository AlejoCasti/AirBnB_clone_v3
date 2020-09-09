#!/usr/bin/python3
''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from json import loads


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def route_state():
    ''' all state's object '''
    lista = [obj.to_dict() for obj in list(storage.all(State).values())]
    return jsonify(lista)


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def route_state_id(id):
    ''' search a state with specific id '''
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<id>', strict_slashes=False, methods=['DELETE'])
def route_state_delete(id):
    ''' delete object '''
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def route_state_post():
    ''' post object '''
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in req:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**req)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<id>', strict_slashes=False, methods=['PUT'])
def route_state_put(id):
    ''' search a state with specific id '''
    ignore_values = ['id', 'created_at', 'updated_at']
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(State, id)
    if obj is None:
        abort(404)
    for key, value in req.items():
        if key not in ignore_values:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
