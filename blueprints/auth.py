from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
from utils.db import query_db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username is not None and password is not None:
            user = query_db('SELECT * FROM users WHERE name = ?', [username], True)

            if user is not None:
                if check_password_hash(user['password'], password):
                    session['id'] = user['id']
                    session['username'] = user['name']
                    session['password'] = user['password']
                    session['grade'] = user['grade']
                    session['logged'] = True

                    if request.form['next'] is not None:
                        return redirect(request.form['next'])
                    else:
                        return redirect('/')
                else:
                    return render_template('error.html', error_code=1000, error_content="Votre nom d'utilisateur "
                                                                                        "ou votre mot de passe est "
                                                                                        "incorrect")
            return render_template('error.html', error_code=1000, error_content="Le nom d'utilisateur indiqué n'existe "
                                                                                "pas")
        else:
            return render_template('error.html', error_code=1000, error_content="Certains paramètres sont manquants")
    else:
        next_dest = '/'
        if 'next' in request.args:
            next_dest = request.args['next']

        return render_template('login.html', session=session, next=next_dest)


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
