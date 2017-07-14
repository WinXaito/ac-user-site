from flask import session, request, redirect, url_for, abort
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged' not in session or not session['logged']:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged' not in session or not session['logged'] or session['grade'] != 4:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
