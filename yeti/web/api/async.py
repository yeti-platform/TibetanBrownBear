
from flask_classful import FlaskView, route
from flask import request
from marshmallow import fields
from rq import Queue
import redis
from webargs.flaskparser import parser

from yeti.core.async import functions
from yeti.common.config import yeti_config
from ..helpers import as_json

# We need to import modules without referencing them so that any async jobs they
# register is actually registered
# pylint: disable=unused-import,wrong-import-order
from yeti import feeds

try:
    redis_connection = redis.Redis(host=yeti_config.async.redis_server,
                                   port=yeti_config.async.redis_port)
    # Set a dummy key to actually trigger the connction.
    redis_connection.set('yeti', 'redis_init')
    q = Queue(connection=redis_connection)
except redis.exceptions.ConnectionError as err:
    raise RuntimeError('Could not establish connection '
                       'to Redis server: ' + str(err))

class AsyncResource(FlaskView):

    route_base = '/async/'

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    def get_registered_asyncjobs(self, name_filter=None):
        function_list = []
        for name, cls in functions.items():
            if name_filter in name:
                obj = cls()
                function_list.append(obj.dump())
        return function_list

    def get_active_asyncjobs(self, name_filter=None):
        job_list = []
        for job in q.jobs:
            if name_filter in j.meta['name']:
                job_list.append({'id': job.id, 'meta': j.meta})
        return job_list

    @as_json
    @route('/filter', methods=['POST'])
    def filter(self):
        """Filters and returns a list of all declared AsyncJobs."""
        args = parser.parse(self.searchargs, request)
        return self.get_registered_asyncjobs(args.name)

    # Async-specific endpoints

    @as_json
    @route('/<name>/toggle', methods=['POST'])
    def toggle(self, name):
        """Toggles the enabled state of a registered AsyncJob."""
        if name not in functions:
            return {
                'error': '{0:s} is not a registered AsyncJob'.format(name)
            }, 404
        job = functions[name]()
        job.toggle()
        return {
            'msg': '{0:s} enabled: {1:s}'.format(name, job.settings.enabled),
            'enabled': job.settings.enabled
        }

    @as_json
    @route('/<name>/execute', methods=['POST'])
    def execute(self, name):
        """Executes a declared AsyncJob by name.

        Returns:
            Dictionary containing a message, the Job ID of the
            created job and its current status.
        """
        if name not in functions:
            return {
                'error': '{0:s} not a registered AsyncJob'.format(name)
            }, 404
        jobs = self.get_active_asyncjobs(name_filter=name)
        if jobs:
            return {
                'error': 'Jobs ~ {0:s} are already running'.format(name),
                'job_details': jobs,
            }, 409

        job = q.enqueue(functions[name].create)
        job.meta['name'] = name
        job.save_meta()
        return {
            'msg': "Job '{0:s}' enqueued succesfully".format(name),
            'job_id': job.get_id(),
            'status': job.get_status(),
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
        if not job:
            return {
                'error': 'Job ID {0:s} is not an active job'.format(job_id)
            }, 404
        return {
            'result': job.result,
            'status': job.get_status(),
            'meta': job.meta
            }

    @as_json
    @route('/active', methods=['GET'])
    def active(self):
        """Returns a list of all active jobs in queue."""
        return self.get_active_asyncjobs()
