from src.libs.status_code import HttpStatusCode


class CoreException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Exception: {self.message}'


class BaseRequestException(CoreException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class RequestMethodNotAllowed(BaseRequestException):
    def __init__(self, message: str):
        super().__init__(message, status_code=HttpStatusCode.METHOD_NOT_ALLOWED)


class InvalidInputDataException(CoreException):
    pass
