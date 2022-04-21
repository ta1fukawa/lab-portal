import base64
import datetime
import hashlib
import urllib.parse
import threading

import dateutil.relativedelta
import flask
import flask_cors
import mysql.connector

from tcu_portal import TcuPortal

with open('/run/secrets/db_root_passwd', 'r') as f:
    db_root_passwd = f.read().strip()

db = mysql.connector.connect(
    host="db",
    user="root",
    passwd=db_root_passwd,
    database="portal",
    buffered=True,
)

def db_ping():
    try:
        # db.ping(reconnect=True)
        db.cursor().execute("SELECT user()").fetchone()
    except:
        pass
    finally:
        threading.Timer(60, db_ping).start()

threading.Thread(target=db_ping).start()

app = flask.Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
flask_cors.CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

def get_request_data(request):
    if request.method == 'GET':
        request_data = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query, keep_blank_values=True)
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            request_data = request.get_json()
        else:
            request_data = request.form
    else:
        request_data = {}
    return request_data

def chech_user_by_tcu_account(user_id, password):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id as user_id, name, email FROM users INNER JOIN user_tcu_account ON users.id = user_tcu_account.user_id WHERE user_tcu_account.username = %s AND user_tcu_account.password = %s AND users.removed_at IS NULL", (user_id, password))
    return cursor.fetchone()

def calc_password_hash(password, salt):
    hs = '{SSHA}' + base64.b64encode(hashlib.sha1(password.encode('utf-8') + salt).digest() + salt).decode('utf-8')
    return hs

@app.route('/login', methods=['GET', 'POST'])
def login():
    request_data = get_request_data(flask.request)

    if 'username' not in request_data or 'password' not in request_data:
        return flask.jsonify({'success': False, 'message': 'ユーザ名とパスワードを指定してください。'})

    username = request_data['username'][0] if type(request_data['username']) == list else request_data['username']
    password = request_data['password'][0] if type(request_data['password']) == list else request_data['password']
    account = chech_user_by_tcu_account(username, password)
    if not account:
        return flask.jsonify({'success': False, 'message': 'ユーザ名またはパスワードが間違っています。'})
    flask.session.permanent = True
    flask.session['user_id'] = account['user_id']
    return flask.jsonify({'success': True, 'data': {'username': username}})

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    request_data = get_request_data(flask.request)

    if 'name' not in request_data or 'email' not in request_data:
        return flask.jsonify({'success': False, 'message': '名前とメールアドレスを指定してください。'})
    
    name = request_data['name'][0] if type(request_data['name']) == list else request_data['name']
    email = request_data['email'][0] if type(request_data['email']) == list else request_data['email']

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return flask.jsonify({'success': False, 'message': '既に登録されているメールアドレスです。'})
    
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    db.commit()

    cursor.execute("SELECT id FROM users WHERE email = %s AND removed_at IS NULL", (email,))
    user_id = cursor.fetchone()['id']
    
    flask.session.permanent = True
    flask.session['user_id'] = user_id
    return flask.jsonify({'success': True, 'data': {}})

@app.before_request
def before_request():
    if 'user_id' in flask.session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE id = %s AND removed_at IS NULL", (flask.session['user_id'],))
        if not cursor.fetchone():
            flask.session.clear()
            return flask.redirect('/login')
        return
    elif flask.request.path in ['/login', '/add-user']:
        return
    else:
        return flask.jsonify({'success': False, 'message': 'ログインしてください。'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask.session.clear()
    return flask.jsonify({'success': True, 'data': {}})

@app.route('/set-tcu-account', methods=['GET', 'POST'])
def set_tcu_account():
    request_data = get_request_data(flask.request)

    if 'username' not in request_data or 'password' not in request_data:
        return flask.jsonify({'success': False, 'message': 'ユーザ名とパスワードを指定してください。'})

    username = request_data['username'][0] if type(request_data['username']) == list else request_data['username']
    password = request_data['password'][0] if type(request_data['password']) == list else request_data['password']

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT user_id FROM user_tcu_account WHERE username = %s AND user_id <> %s", (username, flask.session['user_id']))
    if cursor.fetchone():
        return flask.jsonify({'success': False, 'message': 'このTCUアカウントは別のユーザによって既に登録されています。'})

    cursor.execute("SELECT hash_password FROM tcu_account WHERE username = %s", (username,))
    account = cursor.fetchone()
    if not account:
        return flask.jsonify({'success': False, 'message': 'TCUアカウントが見つかりません。'})

    salt = base64.b64decode(account['hash_password'][6:])[-6:]
    if calc_password_hash(password, salt) != account['hash_password']:
        return flask.jsonify({'success': False, 'message': 'TCUアカウントまたはパスワードが間違っています。'})

    cursor.execute("DELETE FROM user_tcu_account WHERE user_id = %s", (flask.session['user_id'],))
    cursor.execute("INSERT INTO user_tcu_account (user_id, username, password) VALUES (%s, %s, %s)", (flask.session['user_id'], username, password))
    db.commit()

    return flask.jsonify({'success': True, 'data': {}})

@app.route('/get-tcu-account', methods=['GET', 'POST'])
def get_tcu_account():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username, password FROM user_tcu_account WHERE user_id = %s", (flask.session['user_id'],))
    account = cursor.fetchone()
    if not account:
        return flask.jsonify({'success': False, 'message': 'TCUアカウントが登録されていません。'})
    return flask.jsonify({'success': True, 'data': {'username': account['username'], 'password': account['password']}})

@app.route('/remove-tcu-account', methods=['GET', 'POST'])
def remove_tcu_account():
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM user_tcu_account WHERE user_id = %s", (flask.session['user_id'],))
    db.commit()
    return flask.jsonify({'success': True, 'data': {}})

@app.route('/all-users', methods=['GET', 'POST'])
def all_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_full_view")
    return flask.jsonify(cursor.fetchall())

@app.route('/tcu-portal', methods=['GET', 'POST'])
def tcu_portal():
    request_data = get_request_data(flask.request)

    if 'type' not in request_data:
        return flask.jsonify({'success': False, 'message': 'typeを指定してください。'})
    types = request_data['type'][0].split(',')

    if 'since' in request_data:
        since = datetime.strptime(request_data['since'][0], '%Y-%m-%d')
    else:
        since = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)

    if 'until' in request_data:
        until = datetime.strptime(request_data['until'][0], '%Y-%m-%d')
    else:
        until = datetime.datetime.now()

    cursor = db.cursor(dictionary=True)

    data = {}
    if 'message' in types:
        cursor.execute("SELECT id, date, sender, title, is_important, body FROM tcu_portal_message WHERE user_id = %s AND date >= %s AND date <= %s", (flask.session['user_id'], since, until))
        data['message'] = cursor.fetchall()
    if 'oshirase' in types:
        cursor.execute("SELECT id, date, registrant, title, body FROM tcu_portal_oshirase WHERE user_id = %s AND date >= %s AND date <= %s", (flask.session['user_id'], since, until))
        data['oshirase'] = cursor.fetchall()
    if 'daredemo' in types:
        cursor.execute("SELECT id, date, registrant, title, body FROM tcu_portal_daredemo WHERE user_id = %s AND date >= %s AND date <= %s", (flask.session['user_id'], since, until))
        data['daredemo'] = cursor.fetchall()

    return flask.jsonify({'success': True, 'data': data})

@app.route('/tcu-portal-update', methods=['GET', 'POST'])
def tcu_portal_update():
    request_data = get_request_data(flask.request)

    if 'type' not in request_data:
        return flask.jsonify({'success': False, 'message': 'typeを指定してください。'})
    types = request_data['type'][0].split(',')

    if 'since' in request_data:
        since = datetime.strptime(request_data['since'][0], '%Y-%m-%d')
    else:
        since = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)

    if 'until' in request_data:
        until = datetime.strptime(request_data['until'][0], '%Y-%m-%d')
    else:
        until = datetime.datetime.now()
    
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT username, password FROM user_tcu_account WHERE user_id = %s", (flask.session['user_id'],))
        account = cursor.fetchone()
        if not account:
            return flask.jsonify({'success': False, 'message': 'TCUアカウントが登録されていません。'})
        tcu_portal = TcuPortal(account['username'], account['password'], flask.session['user_id'])

        if 'message' in types:
            message_list = tcu_portal.get_message_list(since=since, until=until)
            for message in message_list:
                cursor.execute("SELECT id FROM tcu_portal_message WHERE id = %s", (message['id'],))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO tcu_portal_message (id, user_id, date, sender, title, is_important, body) VALUES (%s, %s, %s, %s, %s, %s, %s)", (message['id'], flask.session['user_id'], message['date'], message['sender'], message['title'], message['important'], message['body']))
                    db.commit()
        if 'oshirase' in types:
            oshirase_list = tcu_portal.get_oshirase_list(since=since, until=until)
            for oshirase in oshirase_list:
                cursor.execute("SELECT id FROM tcu_portal_oshirase WHERE id = %s", (oshirase['id'],))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO tcu_portal_oshirase (id, user_id, date, registrant, title, body) VALUES (%s, %s, %s, %s, %s, %s)", (oshirase['id'], flask.session['user_id'], oshirase['date'], oshirase['registrant'], oshirase['title'], oshirase['body']))
                    db.commit()
        if 'daredemo' in types:
            daredemo_list = tcu_portal.get_daredemo_list(since=since, until=until)
            for daredemo in daredemo_list:
                cursor.execute("SELECT id FROM tcu_portal_daredemo WHERE id = %s", (daredemo['id'],))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO tcu_portal_daredemo (id, user_id, date, registrant, title, body) VALUES (%s, %s, %s, %s, %s, %s)", (daredemo['id'], flask.session['user_id'], daredemo['date'], daredemo['registrant'], daredemo['title'], daredemo['body']))
                    db.commit()

        tcu_portal.logout()
    except Exception as e:
        return flask.jsonify({'success': False, 'message': str(e)})

    return flask.jsonify({'success': True, 'data': {}})

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

    member_list = {}
    for grade, name in grade_table.items():
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_full_view WHERE grade = %s", (grade,))
        members = cursor.fetchall()
        if members:
            for member in members:
                del member['user_id']
            member_list[name] = members

    response = {'success': True, 'data': {'members': member_list}}
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
