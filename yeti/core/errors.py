class GenericYetiError(Exception):
    type = 'GenericYetiError'
    message = 'An error occurred.'
    def __init__(self, message, info=None):
        Exception.__init__(self)
        self.message = message
        if info:
        	self.info = info

class ValidationError(GenericYetiError):
    type = 'ValidationError'


class IntegrityError(GenericYetiError):
    type = 'IntegrityError'
