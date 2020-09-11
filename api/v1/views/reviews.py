#!/usr/bin/python3
''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from json import loads


@app_views.route('/places/<id>/reviews', strict_slashes=False, methods=['GET'])
def route_state_place(id):
    ''' all place's object '''
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in
               place.reviews if obj.place_id == id]
    return jsonify(reviews)


@app_views.route('/reviews/<id>', strict_slashes=False, methods=['GET'])
def route_place_id(id):
    ''' search a place with specific id '''
    obj = storage.get(Review, id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<id>', strict_slashes=False, methods=['DELETE'])
def route_place_delete(id):
    ''' delete object '''
    obj = storage.get(Review, id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<id>/reviews',
                 strict_slashes=False, methods=['POST'])
def route_place_post(id):
    ''' post object '''
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in req:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    print(req)
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if 'text' not in req:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    review = Review(**req)
    setattr(review, 'place_id', id)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<id>', strict_slashes=False, methods=['PUT'])
def route_place_put(id):
    ''' search a place with specific id '''
    ignore_values = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    req = request.get_json()
    if type(req) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(Review, id)
    if obj is None:
        abort(404)
    for key, value in req.items():
        if key not in ignore_values:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
