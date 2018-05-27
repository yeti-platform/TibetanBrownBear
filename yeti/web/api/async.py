from rq import Queue
from redis import Redis
from flask_classful import FlaskView, route
from flask import request
from marshmallow import fields
from webargs.flaskparser import parser

from yeti.core.async import functions
from ..helpers import as_json

# We need to import modules without referencing them so that any async jobs they
# register is actually registered
# pylint: disable=unused-import,wrong-import-order
from yeti import feeds

# TODO(tomchop): Handle connection failures
# TODO(tomchop): This should be optional depending on Yeti configuration
q = Queue(connection=Redis())

class AsyncResource(FlaskView):

    route_base = '/async/'

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }


    @as_json
    @route('/<name>/execute', methods=['POST'])
    def execute(self, name):
        """Executes a declared AsyncJob by name.

        Returns:
            Dictionary containing a message and the Job ID of the
            created job.
        """
        job = q.enqueue(functions[name].create)
        job.meta['name'] = name
        job.save_meta()
        return {
            'result': "Job '{0:s}' enqueued succesfully".format(name),
            'job_id': job.get_id()
            }

    @as_json
    @route('/info/<job_id>', methods=['GET'])
    def info(self, job_id):
        """Fetches runtime information on a specific job.

        Args:
            job_id: The Job ID of the created Job (UUID).

        Returns:
            A dictionary containing job information.
        """
        job = q.fetch_job(job_id)
        return {
            'result': job.result,
            'status': job.get_status(),
            'meta': job.meta
            }

    @as_json
    @route('/active', methods=['GET'])
    def active(self):
        """Returns a list of all active jobs in queue."""
        return [{'id': j.id, 'meta': j.meta} for j in q.jobs]


    @as_json
    @route('/filter', methods=['POST'])
    def filter(self):
        """Filters and returns a list of all declared AsyncJobs."""
        args = parser.parse(self.searchargs, request)
        function_list = []
        for name, cls in functions.items():
            if args['name'] in name:
                obj = cls()
                function_list.append(obj.dump())
        return function_list
