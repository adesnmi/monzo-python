"""
The module that represents any HTTP request related logic.
"""
import requests
from monzo.errors import (BadRequestError, UnauthorizedError, ForbiddenError,
MethodNotAllowedError, PageNotFoundError, NotAcceptibleError,TooManyRequestsError,
InternalServerError, GatewayTimeoutError)

class Request(object):
    """Encapsulates the requests library with Monzo-specific validation."""
    def get(self, url, headers=None, params=None):
        """Sends a GET request to a specified URL

           :param url: The URL to send the request to
           :param headers: The headers to include with the request
           :param params: The data to include with the request

           :rtype: A Dictionary representation of the response
        """
        response = requests.get(url=url, headers=headers, params=params)
        return self.validate_response(response)

    def post(self, url, headers=None, params=None, data=None):
        """Sends a POST request to a specified URL

           :param url: The URL to send the request to
           :param headers: The headers to include with the request
           :param params: The data to include with the request

           :rtype: A Dictionary representation of the response
        """
        response = requests.post(url=url, headers=headers, data=data, params=params)
        return self.validate_response(response)

    def put(self, url, headers=None, params=None, data=None):
        """Sends a PUT request to a specified URL

           :param url: The URL to send the request to
           :param headers: The headers to include with the request
           :param params: The data to include with the request

           :rtype: A Dictionary representation of the response
        """
        response = requests.put(url=url, headers=headers, data=data, params=params)
        return self.validate_response(response)

    def delete(self, url, headers=None, params=None, data=None):
        """Sends a DELETE request to a specified URL

           :param url: The URL to send the request to
           :param headers: The headers to include with the request
           :param params: The data to include with the request

           :rtype: A Dictionary representation of the response
        """
        response = requests.delete(url=url, headers=headers, data=data, params=params)
        return self.validate_response(response)

    def validate_response(self, response):
        """Validate the response and raises any appropriate errors.

           :param response: The response to validate
           :rtype: A Dictionary representation of the response, if no errors occured.
        """
        json_response = response.json()
        if response.status_code == 200:
            return json_response
        if response.status_code == 400:
            raise BadRequestError(json_response['message'])
        if response.status_code == 401:
            raise UnauthorizedError(json_response['message'])
        if response.status_code == 403:
            raise ForbiddenError(json_response['message'])
        if response.status_code == 404:
            raise PageNotFoundError(json_response['message'])
        if response.status_code == 405:
            raise MethodNotAllowedError(json_response['message'])
        if response.status_code == 406:
            raise NotAcceptibleError(json_response['message'])
        if response.status_code == 429:
            raise TooManyRequestsError(json_response['message'])
        if response.status_code == 500:
            raise InternalServerError(json_response['message'])
        if response.status_code == 504:
            raise GatewayTimeoutError(json_response['message'])
