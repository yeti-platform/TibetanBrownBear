class GenericYetiError(Exception):
    type = 'GenericYetiError'
    message = 'An error occurred.'

class ValidationError(GenericYetiError):
    type = 'ValidationError'
    def __init__(self, message):
        GenericYetiError.__init__(self)
        self.message = message
