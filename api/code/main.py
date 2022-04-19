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
    cursor.execute("SELECT id as user_id, name, email FROM users INNER JOIN user_tcu_account ON users.id = user_tcu_account.user_id WHERE user_tcu_account.username = %s AND user_tcu_account.password = %s AND users.removed_at IS NULL", (user_id, password))
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
    account = chech_user_by_tcu_account(username, password)
    if not account:
        return flask.jsonify({'success': False, 'message': 'Invalid username or password'})
    flask.session.permanent = True
    flask.session['user_id'] = account['user_id']
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
    grade_table = {
        'Teacher': '教員',
        'Doctor 5': '博士5年',
        'Doctor 4': '博士4年',
        'Doctor 3': '博士3年',
        'Master 2': '修士2年',
        'Master 1': '修士1年',
        'Bachelor 4': '学士4年',
        'Bachelor 3': '学士3年',
        'Bachelor 2': '学士2年',
        'Bachelor 1': '学士1年',
    }

    members = {}
    for grade, name in grade_table.items():
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_full_view WHERE grade = %s", (grade,))
        teachers = cursor.fetchall()
        if teachers:
            members[name] = teachers

    response = {'success': True, 'data': {'members': members}}
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
