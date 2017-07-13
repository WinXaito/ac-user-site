from flask import Blueprint, render_template, redirect, request, url_for
from blueprints.users import add_user
from dynaconf import settings
import os

install = Blueprint('install', __name__)
APP_ROOT = os.path.dirname(__file__)


@install.route('/install')
def install_view():
    if settings.INSTALL:
        return redirect(url_for('home'))

    return render_template('install.html')


@install.route('/install/setadmin', methods=['POST'])
def install_admin():
    if settings.INSTALL:
        print('Already installed')
        return redirect(url_for('home'))

    if 'username' in request.form and 'password' in request.form:
        add_user(request.form['username'], request.form['password'], grade=4, url_dest='home')
        settings.INSTALL = True
        return redirect(url_for('home'))
    else:
        return redirect(url_for('install.install_view'))
