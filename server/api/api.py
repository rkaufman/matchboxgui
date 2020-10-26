import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt import JWT, jwt_required

from .db import get_user, \
    add_user, get_db, init_db, \
    authenticate_user, get_user_by_id, \
    get_users, get_settings, get_settings_categories, \
    create_setting_category, get_detectors, get_settings_by_category


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
if x is None:
    init_db()


def authenticate(username, password):
    try:
        user = get_user(username)
        if user and authenticate_user(username, password):
            return user
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return jsonify(response_object), 500


@app.route('/users', methods=['POST'])
@jwt_required()
def add_user():
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
        u = get_users()
        return json.dumps(u), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Failed to get users'}), 500


@app.route('/logout', methods=['POST'])
def logout():
    # TODO: add passed in jwt to blacklist
    return jsonify({'status': 'success', 'message': 'logged out'}), 200


@app.route('/setting', methods=['GET'])
def get_setting():
    try:
        settings = get_settings()
        ret = []
        for stg in settings:
            dto = json.dumps(stg, default=lambda s: s.__dict__, indent=4)
            ret.append(dto)
        return jsonify(ret), 200
    except Exception as ex:
        print(ex)
        return jsonify({'status': 'fail', 'message': 'Failed to get settings from the database'}), 500

@app.route('/setting/category/<catId>')
def get_settings_by_cat_id(catId):
    try:
        settings = get_settings_by_category(catId)
        ret = []
        for stg in settings:
            dto = json.dumps(stg, default=lambda s: s.__dict__, indent=4)
            ret.append(dto)
        return jsonify(ret), 200
    except Exception as ex:
        print(ex)
        return jsonify({'status': 'fail', 'message': 'Failed to get settings from the database'}), 500
          


@app.route('/setting/category', methods=['GET'])
def get_setting_catgories():
    try:
        categories = get_settings_categories()
        return json.dumps(categories), 200
    except Exception as ex:
        print(ex)
        return jsonify({'status': 'fail', 'message': 'Failed to get categories'}), 500


@app.route('/setting/category', methods=['POST'])
def add_setting_category():
    try:
        data = json.loads(request.data)
        data.id = create_setting_category(data)
        return jsonify(data), 200
    except Exception as ex:
        return jsonify({'status': 'fail'}), 500

@app.route('/setting/detectors', methods=['GET'])
def get_detector():
    try:
        detectors = get_detectors()
        return json.dumps(detectors), 200
    except Exception as ex:
        return jsonify({'status': 'fail'}),  500