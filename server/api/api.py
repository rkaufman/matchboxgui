from flask import Flask, request, jsonify
from flask_cors import CORS
from .middlewares import login_required
import time
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from .db import get_user, add_user, delete_user, get_db, init_db, authenticate_user
import json

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

x = get_db()
if(x is None):
    init_db()


@app.route("/time", methods=["GET"])
@login_required
def get_current_time():
    return jsonify({"time": time.time()})

@app.route('/users/authenticate', methods=['POST'])
def authenticate():
    data = json.loads(request.data)
    print(data)
    try:
        user = get_user(data.get('username'))
        print(user)
        if user and authenticate_user(data.get('username'), data.get('password')):
            auth_token = encode_auth_token(user['id'])
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(responseObject), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(responseObject), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return jsonify(responseObject), 500

@app.route('/users', methods=['POST'])
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
        return jsonify({'status': 'fail', 'message': 'Failed to create individual'})


def encode_auth_token(self, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    print(user_id)
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
