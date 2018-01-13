#!/usr/bin/env python

"""Main Yeti web module."""

from flask import Flask, url_for
from web.api.api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api')


@app.route('/list_routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    for line in sorted(output):
        print(line)

    return "<br>".join(output)

app.debug = True
app.run()
