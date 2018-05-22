from rq import Queue
from redis import Redis
from flask_classful import FlaskView, route

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

    @as_json
    @route('/<name>/execute', methods=['POST'])
    def execute(self, name):
        job = q.enqueue(functions[name].create)
        job.meta['name'] = name
        job.save_meta()
        return {
            'result': "Job '{0:s}' enqueued succesfully".format(name),
            'job_id': job.get_id()
            }

    @as_json
    @route('/jobinfo/<job_id>', methods=['GET'])
    def jobinfo(self, job_id):
        job = q.fetch_job(job_id)
        return {
            'result': job.result,
            'status': job.get_status(),
            'meta': job.meta
            }

    @as_json
    @route('/joblist', methods=['GET'])
    def joblist(self):
        return [{'id': j.id, 'meta': j.meta} for j in q.jobs]
