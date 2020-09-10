#!/usr/bin/python3
"""
Objects that handles all default RestFul API actions
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    List of all amenities
    """
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<id>/', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    """
    An amenity
    """
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())
