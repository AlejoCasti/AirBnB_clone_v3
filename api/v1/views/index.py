''' routes and views of web page '''
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def route_status():
    ''' return status of app '''
    return jsonify({'status': 'OK'})
