
from flask_classful import FlaskView, route
from flask import request
from marshmallow import fields
from webargs.flaskparser import parser

from yeti.core.asyncjob import functions, q, get_active_jobs
from yeti.core.errors import GenericYetiError
from ..helpers import as_json, auth_required

# We need to import modules without referencing them so that any async jobs
# they register is actually registered
# pylint: disable=unused-import,wrong-import-order
from yeti import feeds


class AsyncResource(FlaskView):

    route_base = '/async/'

    searchargs = {
        'name': fields.Str(required=True),
        'type': fields.Str(),
    }

    def get_registered_asyncjobs(self, name_filter=None):
        """Gets all registered AsyncJobs, filetered by name.

        Args:
            name_filter: String to filter the AsyncJobs' names on.
        """
        function_list = []
        for name, cls in functions.items():
            if name_filter in name:
                obj = cls()
                function_list.append(obj.dump())
        return function_list

    def get_queued_asyncjobs(self, name_filter=None):
        """Gets currently running jobs, filetered by name.

        Args:
            name_filter: String to filter the running jobs' names on.
        """
        job_list = [{
            'id': job.id,
            'meta': job.meta,
            'status': job.get_status()
            } for job in q.jobs]
        if name_filter:
            return [j for j in job_list if name_filter in j['meta']['name']]
        return job_list

    def get_active_asyncjobs(self, name_filter=None):
        """Gets currently running jobs, filetered by name.

        Args:
            name_filter: String to filter the running jobs' names on.
        """
        job_list = [{
            'id': job.id,
            'meta': job.meta,
            'status': job.get_status()
            } for job in get_active_jobs()]
        if name_filter:
            return [j for j in job_list if name_filter in j['meta']['name']]
        return job_list

    @as_json
    @route('/filter', methods=['POST'])
    @auth_required
    def filter(self):
        """Filters and returns a list of all declared AsyncJobs."""
        try:
            args = parser.parse(self.searchargs, request)
        except GenericYetiError as err:
            return err, 400

        jobs_with_status = []
        for job in self.get_registered_asyncjobs(args['name']):
            running_job = self.get_active_asyncjobs(name_filter=args['name'])
            status = running_job[0]['status'] if running_job else 'idle'
            job['status'] = status
            jobs_with_status.append(job)
        return jobs_with_status

    # Async-specific endpoints

    @as_json
    @route('/<name>/toggle', methods=['POST'])
    @auth_required
    def toggle(self, name):
        """Toggles the enabled state of a registered AsyncJob."""
        if name not in functions:
            msg = '{0:s} is not a registered AsyncJob'.format(name)
            return GenericYetiError(message=msg), 404
        job = functions[name]()
        job.toggle()
        return {
            'msg': '{0:s} enabled: {1!r}'.format(name, job.settings.enabled),
            'enabled': job.settings.enabled
        }

    @as_json
    @route('/<name>/execute', methods=['POST'])
    @auth_required
    def execute(self, name):
        """Executes a declared AsyncJob by name.

        Returns:
            Dictionary containing a message, the Job ID of the
            created job and its current status.
        """
        if name not in functions:
            msg = '{0:s} is not a registered AsyncJob'.format(name)
            return GenericYetiError(message=msg), 404

        active_jobs = self.get_active_asyncjobs(name_filter=name)
        queued_jobs = self.get_queued_asyncjobs(name_filter=name)
        jobs = active_jobs + queued_jobs
        if jobs:
            msg = 'Jobs with name ~"{0:s}" are already running'.format(name)
            info = {'job_details': jobs}
            return GenericYetiError(message=msg, info=info), 409


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
    @auth_required
    def info(self, job_id):
        """Fetches runtime information on a specific job.

        Args:
            job_id: The Job ID of the created Job (UUID).

        Returns:
            A dictionary containing job information.
        """
        job = q.fetch_job(job_id)
        if not job:
            msg = 'Job ID {0:s} is not an active job'.format(job_id)
            return GenericYetiError(message=msg), 404
        return {
            'result': job.result,
            'status': job.get_status(),
            'meta': job.meta
            }

    @as_json
    @route('/active', methods=['GET'])
    @auth_required
    def active(self):
        """Returns a list of all active jobs in queue."""
        return self.get_active_asyncjobs()
