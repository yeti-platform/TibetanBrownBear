from rq import Connection, Worker

with Connection():
    w = Worker(['default'])
    w.work()
