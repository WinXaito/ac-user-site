from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from utils.db import query_db, delete, insert
from utils.decorators import login_required, admin_required

users = Blueprint('users', __name__)


@users.route('/users')
@login_required
@admin_required
def users_view():
    mess = ""
    if 'mess' in request.args:
        mess = request.args['mess']

    list_users = query_db('SELECT * FROM users')
    return render_template('users.html', users=list_users, loc='users', mess=mess)


@users.route('/user/add', methods=['POST'])
@login_required
@admin_required
def user_add():
    if 'username' in request.form and 'password' in request.form:
        return add_user(request.form['username'], request.form['password'])
    else:
        return render_template('error.html', error_code=1000, error_content="Paramètre invalide")


@users.route('/user/remove/<user_id>')
@login_required
@admin_required
def user_remove(user_id):
    delete('users', 'id', user_id)
    return redirect(url_for('users.users_view', mess="L'utilisateur a bien été supprimé"))


def add_user(username, password, grade=0, url_dest='users.users_view'):
    if username and password:
        if not query_db('SELECT * FROM users WHERE name = ?', [username], True):
            insert('users', ['name', 'password', 'grade'], [username, generate_password_hash(password,
                                                                                             method='pbkdf2:sha256',
                                                                                             salt_length=10), grade])
            return redirect(url_for(url_dest, mess="L'utilisateur a bien été ajouté"))
        else:
            return render_template('error.html', error_code=1000, error_content="Le nom d'utilisateur existe déjà")
    else:
        return render_template('error.html', error_code=1000, error_content="Paramètre incomplet")
