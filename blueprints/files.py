# coding: utf-8
from flask import Blueprint, send_file, request, render_template, redirect, session, abort, url_for
from utils.decorators import login_required
from utils.db import query_db, delete, update
import os

files = Blueprint('files', __name__)
APP_ROOT = os.path.dirname(__file__)


@files.route('/file/<id>')
@files.route('/file/<id>.png')
def files_file(id):
    file = query_db('SELECT * FROM files WHERE uniqid = ?', [id], True)
    path = '{}/../files/{}.file'.format(APP_ROOT, id)

    if file is None or not os.path.isfile(path):
        return send_file('{}/../static/file/file_error.png'.format(APP_ROOT), mimetype='image/png')

    update('UPDATE files SET view = view + 1 WHERE uniqid = ?', [id])
    return send_file(path, mimetype='image/png')


@files.route('/file/remove/<id>', methods=['GET', 'POST'])
@login_required
def files_remove(id):
    file = query_db('SELECT * FROM files WHERE uniqid = ?', [id], True)

    if request.method == 'GET':
        return render_template('file_remove.html', file=file)
    else:
        if file is None:
            return abort(404)

        if 'confirm-suppress' in request.form:
            if file['user'] == session['id']:
                delete('files', 'uniqid', file['uniqid'])

                path = '{}/../files/{}.file'.format(APP_ROOT, file['uniqid'])
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError:
                        return render_template('error.html', error_code=1000,
                                               error_content='Une erreur est survenu lors de la suppression du '
                                                             'fichier, mais le fichier à tout de meme été supprimé de '
                                                             'la base de données')
                return redirect(url_for('home'))
            else:
                return abort(403)
        else:
            return render_template('file_remove.html', file=file)
