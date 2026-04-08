class ServiceError(Exception):
    pass


class CategoryNotFoundError(ServiceError):
    pass


class UserAlreadyExistsError(ServiceError):
    pass


class InvalidCredentialsError(ServiceError):
    pass


class InactiveUserError(ServiceError):
    pass
