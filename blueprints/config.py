from flask import Blueprint, render_template, request
from blueprints.users import add_user
from utils.decorators import login_required

config = Blueprint('config', __name__)


@config.route('/config')
@login_required
def config_view():
    return render_template('config.html', loc='config')


@config.route('/config/adduser', methods=['POST'])
@login_required
def config_adduser():
    if 'username' in request.form and 'password' in request.form:
        return add_user(request.form['username'], request.form['password'])
    else:
        return render_template('error.html', error_code=1000, error_content="Paramètre invalide")