#!/usr/bin/python3
''' API start '''

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)
API_HOST = environ.get('HBNB_API_HOST')\
           if environ.get('HBNB_API_HOST') else '0.0.0.0'
API_PORT = environ.get('HBNB_API_PORT')\
           if environ.get('HBNB_API_PORT') else '5000'


@app.teardown_appcontext
def close(error):
    ''' close storage '''
    storage.close()


if __name__ == '__main__':
    ''' main funciton to run flask '''
    app.run(host=API_HOST, port=API_PORT, threaded=True)
