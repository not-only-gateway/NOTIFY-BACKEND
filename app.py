from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import env, requests

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = env.DATABASE + '://' + env.USER + ':' + env.PASSWORD_DB + '@' + env.HOST_NAME + '/' + env.DATABASE_NAME
db = SQLAlchemy(app)
CORS(app)

def authorize(method):
    token = request.headers.get('authorization', None)

    if token is not None:
        request_res = requests.get(
            env.AUTH_ENDPOINT,
            headers={'authorization': token},
            params={
                'method': request.method,
                'path': request.path
            })
        if request_res.status_code == 401:
            return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
        return None
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


from notification.models import Notification
from user.models import User

import notification.views

db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1025)
