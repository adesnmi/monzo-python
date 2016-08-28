"""
The module that represents each possible Monzo API error; documented at:
https://monzo.co.uk/docs/#errors as individual Python errors.
"""
class BadRequestError(Exception):
    """An error to be raised when a request has missing arguments or is malformed."""

class UnauthorizedError(Exception):
    """An error to be raised when a request is not authenticated."""

class ForbiddenError(Exception):
    """An error to be raised when a request has insufficient permissions."""

class MethodNotAllowedError(Exception):
    """An error to be raised when a request is using an incorrect HTTP verb."""

class PageNotFoundError(Exception):
    """An error to be raised when a request requests an endpoint that doesn't exist."""

class NotAcceptibleError(Exception):
    """An error to be raised when an application does not accept the content
    format returned according to the Accept headers sent in the request."""

class TooManyRequestsError(Exception):
    """An error to be raised when an application is exceeding its rate limit.
    Back off, buddy. :p"""

class InternalServerError(Exception):
    """An error with Monzo's servers."""

class GatewayTimeoutError(Exception):
    """A timeout has occured on Monzo's servers."""
