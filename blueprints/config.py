from flask import Blueprint, render_template, request, redirect
from utils.db import insert, query_db
from utils.functions import token_generator

config = Blueprint('config', __name__)


@config.route('/config')
def config_view():
    return render_template('config.html', loc='config')


@config.route('/config/adduser', methods=['POST'])
def config_adduser():
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        if username and password:
            if not query_db('SELECT * FROM users WHERE name = ?', [username], True):
                print(insert('users', ['name', 'password', 'grade', 'token'], [username, password, 0, token_generator()]))
                return redirect('/config')
            else:
                return render_template('error.html', error_code=1000, error_content="Le nom d'utilisateur existe déjà")
        else:
            return render_template('error.html', error_code=1000, error_content="Paramètre incomplet")
    else:
        return render_template('error.html', error_code=1000, error_content="Paramètre invalide")