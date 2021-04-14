class EmptyValueException(Exception):
    """EmptyValueException class."""

    def __init__(self, parameter=''):
        self.message = 'The {} parameter is empty.'.format(parameter)
        super().__init__(self.message)
