from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from utils.db import query_db, delete, insert
from utils.decorators import login_required

users = Blueprint('users', __name__)


@users.route('/users')
@login_required
def users_view():
    list_users = query_db('SELECT * FROM users')
    return render_template('users.html', users=list_users, loc='users')


@users.route('/user/remove/<user_id>')
@login_required
def user_remove(user_id):
    user = query_db('')

    delete('users', 'id', user_id)

    return redirect(url_for('users.users_view'))


def add_user(username, password, grade=0, url_dest='config.config_view'):
    if username and password:
        if not query_db('SELECT * FROM users WHERE name = ?', [username], True):
            insert('users', ['name', 'password', 'grade'], [username, generate_password_hash(password,
                                                                                             method='pbkdf2:sha256',
                                                                                             salt_length=10), grade])
            return redirect(url_for(url_dest))
        else:
            return render_template('error.html', error_code=1000, error_content="Le nom d'utilisateur existe déjà")
    else:
        return render_template('error.html', error_code=1000, error_content="Paramètre incomplet")
