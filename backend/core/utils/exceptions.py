class AppException(Exception):
    message = None

    def __init__(self, message, *args: object) -> None:
        self.message = f"{self.__class__.__name__}: {message}"
        super().__init__(message, *args)


class UnimplementedException(AppException):
    pass


class UnhandledExcpetion(AppException):
    pass
