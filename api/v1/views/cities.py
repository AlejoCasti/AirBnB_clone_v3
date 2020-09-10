#!/usr/bin/python3
''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State
from json import loads


@app_views.route('/states/<id>/cities', strict_slashes=False, methods=['GET'])
def route_state_city(id):
    ''' all city's object '''
    state = storage.get(State, id)
    if state is None:
        abort(404)
    cities = [obj.to_dict() for obj in
              state.cities if obj.state_id == id]
    return jsonify(cities)


@app_views.route('/cities/<id>', strict_slashes=False, methods=['GET'])
def route_city_id(id):
    ''' search a city with specific id '''
    obj = storage.get(City, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<id>', strict_slashes=False, methods=['DELETE'])
def route_city_delete(id):
    ''' delete object '''
    obj = storage.get(City, id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<id>/cities', strict_slashes=False, methods=['POST'])
def route_city_post(id):
    ''' post object '''
    state = storage.get(State, id)
    if not state:
        abort(404)
    req = request.get_json()
    if type(req) is not dict:
        abort(400, description="Not a JSON")
    if 'name' not in req:
        abort(400, description="Missing name")
    city = City(**req)
    setattr(city, 'state_id', id)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<id>', strict_slashes=False, methods=['PUT'])
def route_city_put(id):
    ''' search a city with specific id '''
    ignore_values = ['id', 'created_at', 'updated_at', 'state_id']
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(City, id)
    if obj is None:
        abort(404)
    for key, value in req.items():
        if key not in ignore_values:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
