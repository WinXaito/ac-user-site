# coding: utf-8
from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from utils.db import query_db, update
from utils.decorators import login_required

config = Blueprint('config', __name__)


@config.route('/config')
@login_required
def config_view():
    mess = ""
    if 'mess' in request.args:
        mess = request.args['mess']

    return render_template('config.html', loc='config', mess=mess)


@config.route('/config/changepassword', methods=['POST'])
@login_required
def config_changepassword():
    if 'oldpassword' in request.form and 'newpassword' in request.form and 'repeatpassword' in request.form:
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        repeatpassword = request.form['repeatpassword']

        user = query_db('SELECT * FROM users WHERE id = ?', [session['id']], True)

        if user is not None:
            if check_password_hash(user['password'], oldpassword):
                if newpassword == repeatpassword:
                    update('UPDATE users SET password = ? WHERE id = ?',
                           [generate_password_hash(newpassword,
                                                   method='pbkdf2:sha256',
                                                   salt_length=10),
                            session['id']])
                    return redirect(url_for('config.config_view', mess="Le mot de passe a bien été modifié"))
                else:
                    return render_template('error.html', error_code=1000, error_content="Le nouveau mot de passe "
                                                                                        "ainsi que sa répétition ne "
                                                                                        "correspondent pas")
            else:
                return render_template('error.html', error_code=1000, error_content="L'ancien mot de passe est "
                                                                                    "incorrect")
        else:
            return redirect(url_for('auth.logout'))
    else:
        return render_template('error.html', error_code=1000, error_content="Certains paramètres sont manquants")
