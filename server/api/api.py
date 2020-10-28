import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt import JWT, jwt_required

from .db import get_user, \
    add_user, get_db, init_db, \
    authenticate_user, get_user_by_id, \
    get_users, get_settings, get_settings_categories, \
    create_setting_category, get_detectors, get_settings_by_category, \
    update_setting


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

video_input_modes = [
      { "text": 'Onboard', "id": 1 },
      { "text": 'RTSP', "id": 2 },
      { "text": 'YouTube', "id": 3 },
      { "text": 'File', "id": 4 }
    ];

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
            s = {
                   'name': stg.name,
                   'id': stg.settingId,
                   'setting': stg.setting,
                   'controlType': {'id': stg.controlType.id, 'name': stg.controlType.name},
                   'group': stg.group,
                   'label': stg.label,
                   'placeholder': stg.placeholder,
                   'help': stg.help,
                   'required': stg.required,
                   'step': stg.step,
                   'max': stg.max,
                   'min': stg.min
                }
            if stg.name == 'conn-type':
                for m in video_input_modes:
                   if str(m['id']) == str(stg.setting):
                        s['setting'] = m
            ret.append(s)
        return json.dumps(ret), 200
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

@app.route('/setting', methods=['PATCH'])
def update_settings():
    try:
        settings = json.loads(request.data)
        if len(settings) == 0:
            return jsonify({'status', 'failed'}), 401
        for s in settings:
            update_setting(s['_settingId'],s['_setting'])
        return jsonify({'status':'success'}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'status': 'fail'}), 500

@app.route('/logs')
def logs():
    data = sqlitedb.get_logs()
    return jsonify(LogMessageEncoder().encode(data))

@app.route('/status', methods=['GET'])
def status():
    #
    # Update db for status checks:
    #

    # 1.  Are we logged in to MXSERVER
    (login_success, _, _, _, _, _) = mx.login()
    if login_success is True:
        sqlitedb.update_status(Status(StatusType.SERVER, True, ''))
    else:
        sqlitedb.update_status(Status(StatusType.SERVER, False, ''))

    # 2.  Streaming: update this value elsewhere
        # sqlitedb.update_status(Status(StatusType.STREAM, True, ''))

    # 3.  Detecting: update this value elsewhere
        # sqlitedb.update_status(Status(StatusType.FACEFIND, True, ''))

    # 4.  Searching: if we have opted to search AND we are logged in, lets say
    # we're searching
    should_search = db.get_setting("should-submit-face-searches")
    if login_success is True and should_search is True:
        sqlitedb.update_status(Status(StatusType.SEARCH, True, ''))
    else:
        sqlitedb.update_status(Status(StatusType.SEARCH, False, ''))

    # sqlitedb.delete_all_logs()
    mxserver = sqlitedb.get_setting('mx-host')
    camera = sqlitedb.get_setting('rtsp-url')
    url = ''
    if "@" in camera.setting:
        if '://' in camera.setting:
            st = camera.setting.find("://")
            st = st + 3
        else:
            st = 0
        e = camera.setting.find("@")
        url = camera.setting[:st] + 'XXXXXXXXXX' + camera.setting[e:]
    return render_template('status.html', mxserver=mxserver.setting, camera=url, hostip=mlUtil.get_ip_address())


@app.route('/status/data')
def status_data():
    data = sqlitedb.get_statuses()
    return jsonify(StatusEncoder().encode(data))