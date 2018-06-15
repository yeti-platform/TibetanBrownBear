"""Main Yeti web module."""

from flask import Flask, url_for, render_template
from .web.api.api import blueprint

app = Flask(__name__,
            static_folder='web/frontend/dist/static',
            template_folder='web/frontend/dist')
app.register_blueprint(blueprint, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path): # pylint: disable=unused-argument
    import requests
    return requests.get('http://localhost:8080/' + path).text
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
