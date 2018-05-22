from yeti.core import async


class TestFeed(async.AsyncJob):
    def execute(self):
        print("{0:s} was executed asynchronously".format(self.__class__.__name__))
        return 5

async.functions['TestFeed'] = TestFeed
