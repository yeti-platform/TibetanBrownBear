from time import sleep

from yeti.core import asyncjob

class TestFeed(asyncjob.AsyncJob):
    def execute(self):
        sleep(10)
        print("TestFeed was executed asynchronously")
        return 5

asyncjob.functions['TestFeed'] = TestFeed
