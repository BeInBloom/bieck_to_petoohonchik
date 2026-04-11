class ServiceError(Exception):
    pass


class CategoryNotFoundError(ServiceError):
    pass


class UserAlreadyExistsError(ServiceError):
    # def __init__(self, email: str) -> None:
    #     self.email = email
    pass


class InvalidCredentialsError(ServiceError):
    pass


class InactiveUserError(ServiceError):
    pass
