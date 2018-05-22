from abc import abstractmethod, ABC

functions = {}

class AsyncJob(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @classmethod
    def create(cls, *args, **kwargs):
        job = cls(*args, **kwargs)
        return job.execute()
