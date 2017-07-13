from flask import Blueprint, request, Response
from dicttoxml import dicttoxml
from utils.db import query_db


api_auth = Blueprint('api_auth', __name__)


@api_auth.route('/api/auth', methods=['POST'])
def auth_view():
    output = {'status': 'error', 'code': '1000', 'message': 'No indication', 'server_type': 'unofficial'}

    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = query_db('SELECT * FROM users WHERE name = ?', [username], True)

        if user is not None:
            if user['password'] == password:
                output['status'] = 'ok'
                output['code'] = '1101'
                output['message'] = 'Connexion réussi'
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
