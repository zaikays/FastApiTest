from app.adapters.exceptions.base import InfrastructureError


class AuthenticationError(InfrastructureError):
    pass


class AlreadyAuthenticatedError(InfrastructureError):
    pass


class NotAuthorizedError(InfrastructureError):
    pass
