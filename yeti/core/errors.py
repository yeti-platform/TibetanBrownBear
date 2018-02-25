class GenericYetiError(Exception):
    type = 'GenericYetiError'
    message = 'An error occurred.'
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

class ValidationError(GenericYetiError):
    type = 'ValidationError'


class IntegrityError(GenericYetiError):
    type = 'IntegrityError'
