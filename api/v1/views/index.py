#!/usr/bin/python3
''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/status')
def route_status():
    ''' return status of app '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def route_count():
    ''' count of objects '''
    return jsonify(amenities=storage.count(Amenity),
                   cities=storage.count(City),
                   places=storage.count(Place),
                   reviews=storage.count(Review),
                   states=storage.count(State),
                   users=storage.count(User))
