from flask import Blueprint, render_template
from utils.db import query_db

users = Blueprint('users', __name__)


@users.route('/users')
def users_view():
    list_users = query_db('SELECT * FROM users')
    return render_template('users.html', users=list_users, loc='users')
