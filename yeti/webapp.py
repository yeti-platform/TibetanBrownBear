"""Main Yeti web module."""

from flask import Flask, url_for, render_template
import requests
from .web.api.api import blueprint

app = Flask(__name__,
            static_folder='web/frontend/dist/static',
            template_folder='web/frontend/dist')
app.register_blueprint(blueprint, url_prefix='/api')


# TODO(tomchop): Before releasing, include a script that builds everything
# and includes it in the static folder instead of being rendered through flask
# This setup is only good for development.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # if path:
    # TODO(tomchop): Sort this mess out before coming up with a prod deployment
    return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

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
