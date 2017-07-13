from flask import Blueprint, render_template, request, redirect, session, url_for
from time import time
from utils.functions import uniqid
from utils.db import insert
from utils.decorators import login_required
import imghdr
import os


upload = Blueprint('upload', __name__)
APP_ROOT = os.path.dirname(__file__)


@upload.route("/upload", methods=['POST'])
@login_required
def upload_view():
    if session['logged'] and request.files is not None:
        data_upload = upload_file(request.files, session['id'], 'web')
        if data_upload['status'] != 'ok':
            return render_template('error.html', error_code=1000, error_content=data_upload['error'])
        else:
            return redirect(url_for('home'))
    else:
        return render_template('error.html', error_code=1000, error_content="error:params")


def upload_file(files, user_id, source):
    filename = uniqid()
    output = {'status': 'ok', 'error': '', 'filename': filename}
    target = '{}/../files/{}.file'.format(APP_ROOT, filename)

    i = 0
    for f in files.getlist("file"):
        if i == 0:
            if imghdr.what(f) is not None:
                insert(
                    'files',
                    ['name', 'user', 'created_at', 'uniqid', 'source'],
                    [f.filename, user_id, time(), filename, source]
                )
                print(target)
                f.save(target)
            else:
                output['status'] = 'error'
                output['error'] = 'format'
                return output

        i = i + 1

    return output
