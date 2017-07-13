from flask import Blueprint, request, Response
from dicttoxml import dicttoxml
from utils.db import query_db
from blueprints.upload import upload_file


api_upload = Blueprint('api_upload', __name__)


@api_upload.route('/api/upload', methods=['POST'])
def upload_view():
    output = {'status': 'error', 'code': '1000', 'message': 'No indication'}

    if 'username' in request.form and 'password' in request.form and request.files is not None:
        user = query_db('SELECT * FROM users WHERE name = ?', [request.form['username']], True)

        if user is not None:
            if user['password'] == request.form['password']:
                data_upload = upload_file(request.files, user['id'], 'app')

                if data_upload['status'] == 'ok':
                    output = {
                        'status': 'ok',
                        'message': 'Success',
                        'file': {
                            'user_id': user['id'],
                            'uniqid': data_upload['filename'],
                            'size': '',
                            'created_at': '',
                            'display_link': '{}file/{}.png'.format(request.url_root, data_upload['filename'])
                        }
                    }
                    return Response(dicttoxml(output), mimetype='text/xml')
                else:
                    output['code'] = '1101'
                    output['message'] = 'Erreur serveur: {}'.format(data_upload['error'])
                    return Response(dicttoxml(output), mimetype='text/xml')
            else:
                output['code'] = '1101'
                output['message'] = 'Le mot de passe est incorrect'
                return Response(dicttoxml(output), mimetype='text/xml')
        else:
            output['code'] = '1101'
            output['message'] = "L'utilisateur n'existe pas"
            return Response(dicttoxml(output), mimetype='text/xml')
    else:
        output['code'] = '1101'
        output['message'] = 'Certains paramètres sont manquants'
        return Response(dicttoxml(output), mimetype='text/xml')
