"""Main Yeti web module."""

from flask import Flask, url_for, current_app
from yeti.common.config import yeti_config
from .web.api.api import blueprint

app = Flask(__name__,
            static_folder='web/frontend/dist')
app.register_blueprint(blueprint, url_prefix='/api')

app.secret_key = yeti_config.core.secret_key

app.config.update(
    SESSION_COOKIE_SECURE=False,  # Change when moving to production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path): # pylint: disable=unused-argument
    if path.startswith('css/') or path.startswith('js/'):
        return current_app.send_static_file(path)

    return current_app.send_static_file("index.html")

@app.route('/list_routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = '{:50s} {:20s} {}'.format(rule.endpoint, methods, url)
        output.append(line)

    for line in sorted(output):
        print(line)

    return '<br>'.join(output)
