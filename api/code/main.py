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
    # TODO: check username and password
    flask.session.permanent = True
    flask.session['username'] = username
    flask.session['password'] = password
    return flask.jsonify({'success': True})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask.session.clear()
    return flask.jsonify({'success': True})

@app.route('/is_logged_in')
def is_logged_in():
    if 'username' in flask.session and 'password' in flask.session:
        # TODO: check username and password
        return flask.jsonify({'success': True})
    return flask.jsonify({'success': False})

@app.before_request
def before_request():
    if 'username' in flask.session:
        return
    elif flask.request.path in ['/login', '/is_logged_in']:
        return
    else:
        return flask.jsonify({'success': False, 'message': 'Not logged in'})

@app.route('/test')
def test():
    if app.debug:
        response = {'success': True, 'username': flask.session['username'], 'password': flask.session['password']}
    else:
        response = {'success': True}
    return flask.jsonify(response)
    
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
        response = {'success': True}
        if 'type' in request_data:
            id_ = request_data['id'][0]
            pw  = request_data['pw'][0]
            tcu_portal = TcuPortal(id_, pw)

            if 'message' in request_data['type']:
                response['message'] = tcu_portal.get_message_list(since=since, until=until)
            if 'oshirase' in request_data['type']:
                response['oshirase'] = tcu_portal.get_oshirase_list(since=since, until=until)
            if 'daredemo' in request_data['type']:
                response['daredemo'] = tcu_portal.get_daredemo_list(since=since, until=until)

            tcu_portal.logout()
    except Exception as e:
        response = {'success': False, 'error_message': str(e)}

    return flask.jsonify(response)

@app.route('/lab-members')
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
    response = {'success': True, 'members': members}
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
