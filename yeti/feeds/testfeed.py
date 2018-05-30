from time import sleep

from yeti.core import async

class TestFeed(async.AsyncJob):
    def execute(self):
        sleep(10)
        print("TestFeed was executed asynchronously")
        return 5

async.functions['TestFeed'] = TestFeed
