#!/usr/bin/python3
''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
from models.state import State
from json import loads


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def route_state_user():
    ''' all user's object '''
    users = list(storage.all(User).values())
    dic = [obj.to_dict() for obj in users]
    return jsonify(dic)


@app_views.route('/users/<id>', strict_slashes=False, methods=['GET'])
def route_user_id(id):
    ''' search a user with specific id '''
    obj = storage.get(User, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<id>', strict_slashes=False, methods=['DELETE'])
def route_user_delete(id):
    ''' delete object '''
    obj = storage.get(User, id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def route_user_post():
    ''' post object '''
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in req:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in req:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**req)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<id>', strict_slashes=False, methods=['PUT'])
def route_user_put(id):
    ''' search a user with specific id '''
    ignore_values = ['id', 'created_at', 'updated_at', 'email']
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(User, id)
    if obj is None:
        abort(404)
    for key, value in req.items():
        if key not in ignore_values:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
