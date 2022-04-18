import flask
import flask_cors
import datetime
import urllib.parse
import mysql.connector

import dateutil.relativedelta

from tcu_portal import TcuPortal

with open('/run/secrets/db_root_passwd', 'r') as f:
    db_root_passwd = f.read().strip()
    
db = mysql.connector.connect(
    host="db",
    user="root",
    passwd=db_root_passwd,
    database="portal"
)
db.ping(reconnect=True)

app = flask.Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
flask_cors.CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

def chech_user_by_tcu_account(user_id, password):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id as user_id, name, email FROM users INNER JOIN user_tcu_account ON users.id = user_tcu_account.user_id WHERE user_tcu_account.username = %s AND user_tcu_account.password = %s AND users.removed_at IS NOT NULL", (user_id, password))
    return cursor.fetchone()

@app.route('/login', methods=['GET', 'POST'])
@flask_cors.cross_origin(headers=['Content-Type', 'Authorization'], supports_credentials=True)
def login():
    if flask.request.method == 'GET':
        request_data = urllib.parse.parse_qs(urllib.parse.urlparse(flask.request.url).query, keep_blank_values=True)
    elif flask.request.method == 'POST':
        if flask.request.headers['Content-Type'] == 'application/json':
            request_data = flask.request.get_json()
        else:
            request_data = flask.request.form

    if 'username' not in request_data or 'password' not in request_data:
        return flask.jsonify({'success': False, 'message': 'Missing username or password'})

    username = request_data['username'][0] if type(request_data['username']) == list else request_data['username']
    password = request_data['password'][0] if type(request_data['password']) == list else request_data['password']
    if not chech_user_by_tcu_account(username, password):
        return flask.jsonify({'success': False, 'message': 'Invalid username or password'})
    flask.session.permanent = True
    flask.session['username'] = username
    flask.session['password'] = password
    return flask.jsonify({'success': True, 'data': {'username': username}})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask.session.clear()
    return flask.jsonify({'success': True, 'data': {}})

@app.route('/is_logged_in', methods=['GET', 'POST'])
def is_logged_in():
    if 'username' in flask.session and 'password' in flask.session:
        username = flask.session['username']
        password = flask.session['password']
        if chech_user_by_tcu_account(username, password):
            return flask.jsonify({'success': True, 'data': {'username': flask.session['username']}})
    return flask.jsonify({'success': False, 'message': 'Not logged in'})

@app.before_request
def before_request():
    if 'username' in flask.session:
        return
    elif flask.request.path in ['/login', '/is_logged_in']:
        return
    else:
        return flask.jsonify({'success': False, 'message': 'Not logged in'})

@app.route('/all_users', methods=['GET', 'POST'])
def all_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_full_view")
    return flask.jsonify(cursor.fetchall())

@app.route('/tcu-portal', methods=['GET', 'POST'])
def tcu_portal():
    if flask.request.method == 'GET':
        request_data = urllib.parse.parse_qs(urllib.parse.urlparse(flask.request.url).query, keep_blank_values=True)
    elif flask.request.method == 'POST':
        if flask.request.headers['Content-Type'] == 'application/json':
            request_data = flask.request.get_json()
        else:
            request_data = flask.request.form
    else:
        return flask.jsonify({'success': False, 'error_message': 'ID or PW is not found'})

    if 'id' not in request_data or 'pw' not in request_data:
        return flask.jsonify({'success': False, 'error_message': 'ID or PW is not found'})

    if 'since' in request_data:
        since = datetime.strptime(request_data['since'][0], '%Y-%m-%d')
    else:
        since = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)

    if 'until' in request_data:
        until = datetime.strptime(request_data['until'][0], '%Y-%m-%d')
    else:
        until = datetime.datetime.now()

    try:
        response = {'success': True, 'data': {}}
        if 'type' in request_data:
            id_ = request_data['id'][0]
            pw  = request_data['pw'][0]
            tcu_portal = TcuPortal(id_, pw)

            if 'message' in request_data['type']:
                response['data']['message'] = tcu_portal.get_message_list(since=since, until=until)
            if 'oshirase' in request_data['type']:
                response['data']['oshirase'] = tcu_portal.get_oshirase_list(since=since, until=until)
            if 'daredemo' in request_data['type']:
                response['data']['daredemo'] = tcu_portal.get_daredemo_list(since=since, until=until)

            tcu_portal.logout()
    except Exception as e:
        response = {'success': False, 'message': str(e)}

    return flask.jsonify(response)

@app.route('/lab-members', methods=['GET', 'POST'])
def lab_members():
    members = {
        '教授': [
            {
                'name': '神野 健哉',
                'name_en': 'Kenya Jinno',
                'name_kana': 'ジンノ ケンヤ',
                'position': '教授',
                'image': 'kenya_jinno.jpg',
                'mail': 'kjinno@tcu.ac.jp',
                'twitter_id': '@kjinno',
                'description': '我々のボスである。',
            }
        ],
        'M2': [
            {
                'name': '山田 太郎',
                'name_en': 'Taro Yamada',
                'name_kana': 'ヤマダ タロウ',
                'image': 'dummy.png',
                'tel': '090-1234-5678',
                'description': '我々の一員である。',
            }
        ],
    }
    response = {'success': True, 'data': {'members': members}}
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
