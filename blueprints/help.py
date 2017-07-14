# coding: utf-8
from flask import Blueprint, render_template, Markup, current_app as app
import markdown
import os

help = Blueprint('help', __name__)
APP_ROOT = os.path.dirname(__file__)


@help.route('/help/<path:h>')
def help_view(h):
    path = 'static/help/home.md'
    if h is not None:
        path = 'static/help/{}.md'.format(h)

    if not os.path.isfile('{}/../{}'.format(APP_ROOT, path)):
        return render_template('error.html', error_code=404, error_content="L'aide demandé n'a pas été trouvé")

    with app.app_context():
        with app.open_resource(path, mode='r') as f:
            content = Markup(markdown.markdown(f.read(), extensions=["markdown.extensions.fenced_code"]))

    return render_template('help.html', loc='help', help_content=content)
