# coding: utf-8
from flask import Blueprint, send_file
import os

files = Blueprint('files', __name__)
APP_ROOT = os.path.dirname(__file__)


@files.route('/file/<id>')
@files.route('/file/<id>.png')
def files_file(id):
    return send_file('{}/../files/{}.file'.format(APP_ROOT, id), mimetype='image/png')
