from flask import Flask, request, jsonify
from flask_cors import CORS
from .middlewares import login_required
import time
import os
from .db import get_user, add_user, delete_user, get_db, init_db, authenticate_user, get_user_by_id, get_users
import json
import datetime
from flask_jwt import JWT, jwt_required

def identity(payload):
    print(payload)
    user_id = payload['identity']
    return get_user_by_id(user_id)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
CORS(app)
jwt = JWT(app, authenticate_user, identity)

x = get_db()
if(x is None):
    init_db()

@app.route("/time", methods=["GET"])
@jwt_required()
def get_current_time():
    return jsonify({"time": time.time()})

def authenticate(username, password):
    print('username')
    print('password')
    try:
        user = get_user(data.get('username'))
        if user and authenticate_user(data.get('username'), data.get('password')):
            return user
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return jsonify(responseObject), 500

@app.route('/users', methods=['POST'])
@jwt_required()
def addUser():
    try:
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')
        add_user(username, password)
        return jsonify({'status': 'created',
        'message': 'Successfully added user.'}), 201
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Failed to create user'})

@app.route('/users', methods=['GET'])
@jwt_required()
def users():
    try:
        users = get_users()
        return json.dumps(users), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Failed to get users'}), 500

