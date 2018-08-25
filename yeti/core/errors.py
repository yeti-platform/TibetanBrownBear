class GenericYetiError(Exception):
    type = 'GenericYetiError'
    message = 'An error occurred.'
    def __init__(self, message, info=None):
        super().__init__(message)
        self.message = message
        if info:
            self.info = info


class ValidationError(GenericYetiError):
    type = 'ValidationError'


class IntegrityError(GenericYetiError):
    type = 'IntegrityError'


class RuntimeException(GenericYetiError):
    type = 'RuntimeError'


class YetiSTIXError(GenericYetiError):
    type = 'YetiSTIXError'
