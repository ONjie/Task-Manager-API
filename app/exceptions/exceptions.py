class UserNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TaskNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidPasswordException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TokenNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)