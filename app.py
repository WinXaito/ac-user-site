# coding: utf-8
from flask import Flask, render_template, request, redirect, session, g, url_for
from blueprints.install import install
from blueprints.auth import auth
from blueprints.config import config
from blueprints.upload import upload
from blueprints.users import users
from blueprints.files import files
from blueprints.api.auth import api_auth
from blueprints.api.upload import api_upload
from blueprints.help import help
from utils.db import query_db, init_db
from dynaconf import settings
from utils.decorators import login_required
import os
import utils.functions as func

# Init app
app = Flask(__name__)
app.config.from_object('config.DevConfig')
APP_ROOT = os.path.dirname(__file__)

# Blueprints
app.register_blueprint(install)
app.register_blueprint(auth)
app.register_blueprint(config)
app.register_blueprint(upload)
app.register_blueprint(files)
app.register_blueprint(users)
app.register_blueprint(api_auth)
app.register_blueprint(api_upload)
app.register_blueprint(help)

# Filters
app.add_template_filter(func.basename)

# Database initialisation
os.environ['DYNACONF_INSTALL'] = '@bool true'
os.environ['DYNACONF_INSTALL_DATABASE'] = '@bool false'
with app.app_context():
    if not os.path.isfile('{}/database.db'.format(APP_ROOT)):
        settings.INSTALL = False

        if not settings.INSTALL_DATABASE:
            init_db()
            settings.INSTALL_DATABASE = True
    elif len(query_db('SELECT * FROM users', [], False)) < 1:
        settings.INSTALL = False


@app.before_request
def before_request():
    no_redirects = {
        'install.install_view',
        'install.install_admin',
        'static'
    }

    if request.endpoint not in no_redirects:
        if not settings.INSTALL:
            return redirect(url_for('install.install_view'))


@app.context_processor
def global_variables():
    return dict(version=app.config['VERSION'], session=session)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


@app.errorhandler(403)
def error_403(e):
    return render_template('error.html', error_code=403, error_content="Accès refusé", error_detail=e)


@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error_code=404, error_content="Page non trouvé", error_detail=e)


@app.route('/')
@login_required
def home():
    page = 0
    request_page = request.args.get('p')
    if request_page is not None and func.represents_int(request_page):
        page = int(request_page)

    files = query_db('SELECT * FROM files WHERE user = ? ORDER BY created_at DESC', [session['id']], False)
    return render_template('index.html', files=files, page=page, session=session, loc='home')


if __name__ == '__main__':
    app.run()
