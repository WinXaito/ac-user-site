from flask import Flask, render_template, request, send_file, redirect, session, g, Blueprint
from blueprints.install import install
from blueprints.config import config
from blueprints.upload import upload
from blueprints.users import users
from blueprints.api.auth import api_auth
from blueprints.api.upload import api_upload
from utils.db import query_db
import os
import utils.functions as func

app = Flask(__name__)
app.config.from_object('config.DevConfig')
APP_ROOT = os.path.dirname(__file__)

app.register_blueprint(install)
app.register_blueprint(config)
app.register_blueprint(upload)
app.register_blueprint(users)
app.register_blueprint(api_auth)
app.register_blueprint(api_upload)

app.add_template_filter(func.basename)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    if 'username' not in session:
        return render_template('login.html', session=session)

    page = 0
    requestPage = request.args.get('p')
    if requestPage is not None and func.represents_int(requestPage):
        page = int(requestPage)

    files = query_db('SELECT * FROM files WHERE user = ? ORDER BY created_at DESC', [session['id']], False)
    return render_template('index.html', files=files, page=page, session=session, loc='home')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username is not None and password is not None:
        user = query_db('SELECT * FROM users WHERE name = ? AND password = ?', [username, password], True)

        if user is not None:
            session['id'] = user['id']
            session['username'] = user['name']
            session['password'] = user['password']
            session['grade'] = user['grade']
            session['logged'] = True
            return redirect('/')
        return 'Login error'
    else:
        return 'Login param error'


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/file/<id>')
@app.route('/file/<id>.png')
def file(id):
    return send_file('{}/files/{}.file'.format(APP_ROOT, id), mimetype='image/png')


if __name__ == '__main__':
    app.run()
