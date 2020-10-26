import sqlite3
import click
import os
import datetime
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
import numpy as np
from .setting import Setting
from .control_type import ControlType
from .status import Status
from .log_message import LogMessage
import datetime
from .user import User

DATABASE = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'mxedgesql.db')


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_user_by_id(user_id):
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    u = User(int(user['id']))
    u.username = str(user['username'])
    return u


def get_user(username):
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    u = User(int(user['id']))
    u.username = str(user['username'])
    u.password = str(user['pwd'])
    return u


def get_users():
    db = get_db()
    rows = db.execute(
        'SELECT * FROM users;'
    ).fetchall()
    result = []
    for row in rows:
        result.append({'username': row['username'], 'id': row['id']})
    return result


def get_db():
    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'schema.sql')) as f:
        db.executescript(f.read())
    add_user('admin', 'MXserver1!')


def add_video_url(url, mode):
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM video WHERE video_url =? AND video_input_mode = ?",
                       (str(url), str(mode))).fetchone()[0]
    if count > 0:
        video_id = db.execute("SELECT id FROM video WHERE video_url =? AND video_input_mode = ?",
                              (str(url), str(mode))).fetchone()[0]
        return video_id
    cursor = db.cursor()
    cursor.execute('INSERT INTO video(video_url, video_input_mode) VALUES(?,?)', (str(url), str(mode)));
    video_id = cursor.lastrowid
    db.commit()
    return video_id


def get_video_url():
    db = get_db()
    url = db.execute('SELECT * FROM video ORDER BY id DESC LIMIT 1').fetchone()
    return url


def delete_video_url(video_id):
    db = get_db()
    if video_id is None:
        db.execute('DELETE FROM video')
    else:
        db.execute('DELETE FROM video WHERE id = ?', str(video_id))
    db.commit()


def add_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO users (username,pwd) VALUES (?, ?)', (username, generate_password_hash(password)))
    user_id = cursor.lastrowid
    db.commit()
    return user_id


def authenticate_user(username, password):
    print(username)
    print(password)
    user = get_user(username)
    print(user)
    if check_password_hash(user.password, password):
        print('authenticated')
        user.password = ''
        return user
    else:
        print('not authenticated')
        return False


def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', str(user_id))


def get_settings():
    db = get_db()
    cursor = db.cursor()
    settings = cursor.execute(
        'SELECT * FROM settings ORDER BY sort_order').fetchall()
    result = []
    for row in settings:
        s = create_setting(row)
        result.append(s)
    return result


def get_settings_by_category(catId):
    db = get_db()
    cursor = db.cursor()
    settings = cursor.execute('select * from settings where setting_category_id = ?', str(catId)).fetchall()
    data = []
    for row in settings:
        data.append(create_setting(row))
    return data


def get_setting(key):
    db = get_db()
    setting = db.execute('SELECT * FROM settings WHERE setting_name = ?', (key,)).fetchone()
    if setting is None:
        return None
    data = create_setting(setting)
    return data

def add_child_to_parent_category(c, parent, parents):
    for p in parents:
        if p["id"] == parent:
            p["children"].append(c)
            return True
    return false
        

def get_settings_categories():
    db = get_db()
    rows = db.execute('SELECT * FROM setting_category')
    parents = []
    children = []
    for id,name,icon,route,parent in rows:
        c = {
                "id":id,
                "name": str(name),
                "icon": str(icon),
                "route": str(route),
                "parent": parent,
                "children": []
            }
        if parent > 0:
            print('adding child')
            success = add_child_to_parent_category(c, parent, parents)
            if success == False:
                children.append(c)
        else:
            print(parent)
            parents.append(c);
    if len(children) > 0:
        for ch in children:
            add_child_to_parent_category(ch, children,ch["parent"], parents)
    return parents



def create_setting(row):
    control_types = get_control_types()
    s = Setting(row['setting_name'], row['setting_value'])
    s.settingId = row['id']
    s.group = str(row['setting_category_id'])
    s.controlType = filter_control(row['setting_control_type_id'], control_types)
    s.help = str(row['setting_help'])
    s.label = str(row['setting_label'])
    s.placeholder = str(row['setting_placeholder'])
    s.required = bool(row['setting_required'])
    s.step = str(row['step'])
    s.max = str(row['max_value'])
    s.min = str(row['min_value'])
    return s


def add_setting(setting):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO settings(setting_name, setting_value, setting_tab) values (?,?,?)',
                   (setting.name, str(setting.setting), setting.group))
    setting.settingId = cursor.lastrowid
    return setting


def update_setting(key, value):
    db = get_db()
    db.execute('UPDATE settings SET setting_value = ? WHERE id = ?', (str(value), key))
    db.commit()


def delete_setting(setting_id):
    db = get_db()
    db.execute('DELETE FROM settings WHERE id = ?', str(setting_id))
    db.commit()


def get_control_types():
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute('SELECT * FROM setting_control_types').fetchall()
    data = []
    for r in rows:
        data.append(ControlType(r['id'], r['kind']))
    return data


def filter_control(kind, list):
    for k in list:
        if k.id == kind:
            return k
    return None


def get_statuses():
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute('SELECT * FROM statuses ORDER BY sort_order').fetchall()
    data = []
    for r in rows:
        data.append(Status(r['status_name'], r['status_value'], r['status_display']));
    return data


def get_status(name):
    db = get_db()
    cursor = db.cursor()
    row = cursor.execute('SELECT * FROM statuses WHERE status_name = ?', (name,)).fetchone()
    return Status(row['status_name'], row['status_value'], row['status_display'])


def add_status(status):
    db = get_db()
    db.execute('INSERT INTO statuses(status_name, status_value) VALUES(?,?)', (status.name, status.status))
    db.commit()


def update_status(status):
    current = get_status(str(status.name))
    if current is not None:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE statuses SET status_value = ? WHERE status_name = ?',
                       (str(status.status), str(status.name)))
        db.commit()
    else:
        add_status(status)


def delete_status(name):
    db = get_db()
    db.execute('DELETE FROM statuses WHERE status_name = ?', (name,))
    db.commit()


def get_logs():
    delete_logs()
    db = get_db()
    cursor = db.cursor()
    rows = cursor.execute('SELECT * FROM logs ORDER BY datetime(submitted_date) DESC LIMIT 100').fetchall()
    data = []
    for row in rows:
        data.append(LogMessage(row['log_message'], row['submitted_date']))
    return data


def add_log(logMessage):
    db = get_db()

    if isinstance(logMessage, str):
        db.execute('INSERT INTO logs(submitted_date, log_message) VALUES(?,?)', (datetime.datetime.now(), logMessage))
    else:
        db.execute('INSERT INTO logs(submitted_date, log_message) VALUES(?,?)',
                   (logMessage.submissiondate, logMessage.message))
    db.commit()


def delete_logs():
    db = get_db()
    db.execute('DELETE FROM logs WHERE submitted_date < ?', (datetime.datetime.now() - datetime.timedelta(minutes=30),))
    db.commit()


def delete_all_logs():
    db = get_db()
    db.execute('DELETE FROM logs')
    db.commit()


# telemetry stuff can be removed
def send_frame(fn):
    db = get_db()
    db.execute('insert into telemetry(frame, sent) values(?,?)', (str(fn), datetime.datetime.now()))
    db.commit()


def rec_frame(fn):
    db = get_db()
    db.execute('insert into telemetry(frame, rec) values(?,?)', (str(fn), datetime.datetime.now()))
    db.commit()


def create_setting_category(cat):
    db = get_db()
    db.execute('insert into setting_category(name, parent) values(?,?)', (cat.name, cat.parent))
    db.commit()


def get_detectors():
    db = get_db()
    cursor = db.cursor()
    try:
        rows = cursor.execute('select * from detector').fetchall()
    except Exception as e:
        print(e)
    data = []
    print('looping')
    for id,name,icon in rows:
        data.append({
            "id": id,
            "name": name,
            "icon": icon})
    return data
