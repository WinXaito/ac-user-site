from flask import Blueprint, render_template

install = Blueprint('install', __name__)


@install.route('/install')
def install_view():
    return render_template('install.html')
