#!/usr/bin/python3
''' API start '''

from flask import Flask, jsonify, render_template, make_response
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(error):
    ''' close storage '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    ''' page not found '''
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == '__main__':
    ''' main funciton to run flask '''
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=API_HOST, port=API_PORT, threaded=True)
