from flask import jsonify
from flask import request
import env
from app import app, authorize
from app import db
from notification.models import Notification
import requests
from api.api import ApiView

api = ApiView(
    class_instance=Notification,
    identifier_attr='id',
    relationships=[],
    db=db,
    on_before_call=authorize
)


@app.route('/api/list/notification', methods=['GET'])
def list_data():
    request_res = requests.get(
        env.AUTH_ENDPOINT,
        headers={'authorization': request.headers.get('Authorization', None)},
        params={
            'method': request.method,
            'path': request.path
        })
    json = request_res.json()
    if request_res.status_code == 401:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401

    return api.list(request, base_query=[{'key': 'receiver', 'value': json.get("user_email"), 'type': 'object'}])
