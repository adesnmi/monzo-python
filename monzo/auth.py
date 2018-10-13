"""OAuth2 session client to handle authentication of calls to the Monzo API

Adapted from the implementation for a Fitbit API Python client by Orcas, Inc.
and used under the Apache2 license: https://www.apache.org/licenses/LICENSE-2.0

Original code may be found at: https://github.com/orcasgit/python-fitbit

"""

import json
import requests

from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from monzo.utils import save_token_to_file
from monzo.errors import (BadRequestError, UnauthorizedError, ForbiddenError,
MethodNotAllowedError, PageNotFoundError, NotAcceptibleError,TooManyRequestsError,
InternalServerError, GatewayTimeoutError)

class MonzoOAuth2Client(object):
    AUTHORIZE_ENDPOINT = "https://auth.monzo.com"
    API_ENDPOINT = "https://api.monzo.com"
    API_VERSION = 1

    _authorization_url = AUTHORIZE_ENDPOINT
    _request_token_url = "%s/oauth2/token" % API_ENDPOINT
    _access_token_url = _request_token_url
    _refresh_token_url = _request_token_url

    _localhost = 'http://localhost'

    def __init__(self, client_id, client_secret, access_token=None,
            refresh_token=None, expires_at=None, refresh_callback=save_token_to_file,
            redirect_uri=_localhost, *args, **kwargs):
        """
        Create a MonzoOAuth2Client object.
        Specify the first 7 parameters if you have them to access user data.
        Specify just the first 2 parameters to start the setup for user authorization
        (These are generated at https://developers.monzo.com/)
            
            :param client_id: Client id string as given by Monzo Developer website
            :param client_secret: Client secret string as given by Monzo Developer website
            :param access_token: String token needed to access Monzo API
            :param refresh_token: String token used to refresh expired access token.
            :param expires_at: Unix time representation of access token expiry
            :param refresh_callback: Callback function for when access token is refreshed
            :param redirect_uri: URL to which user is redirected to after authentication by Monzo
        """

        self.client_id, self.client_secret = client_id, client_secret
        token = {}
        if access_token:
            token.update({'access_token': access_token})
        if refresh_token:
            token.update({'refresh_token': refresh_token})
        if expires_at:
            token['expires_at'] = expires_at

        self.session = OAuth2Session(
            client_id,
            auto_refresh_url=self._refresh_token_url,
            token_updater=refresh_callback,
            token=token,
            redirect_uri=redirect_uri,
        )
        self.timeout = kwargs.get("timeout", None)

    def _request(self, method, url, **kwargs):
        """
        A simple wrapper around requests.
        """
        if self.timeout is not None and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        try:
            response = self.session.request(method, url, **kwargs)

            # If our current token has no expires_at, or something manages to slip
            # through that check
            if response.status_code == 401:
                d = json.loads(response.content.decode('utf8'))
                if d['errors'][0]['errorType'] == 'expired_token':
                    self.refresh_token()
                    response = self.session.request(method, url, **kwargs)

            return response
        except requests.Timeout as e:
            pass
            #raise exceptions.Timeout(*e.args)

    def make_request(self, url, data=None, method=None, **kwargs):
        """
        Builds and makes the OAuth2 Request, catches errors
        https://docs.monzo.com/#errors
        """
        data = data or {}
        method = method or ('POST' if data else 'GET')
        response = self._request(
            method,
            url,
            data=data,
            client_id=self.client_id,
            client_secret=self.client_secret,
            **kwargs
        )

        return self.validate_response(response)

    def authorize_token_url(self, redirect_uri = None, **kwargs):
        """Step 1: Return the URL the user needs to go to in order to grant us
        authorization to look at their data.  Then redirect the user to that
        URL, open their browser to it, or tell them to copy the URL into their
        browser.

            :param redirect_uri: url to which the response will posted.
            :rtype: A Tuple consisting of the authentication url and the state token.
        """

        if redirect_uri:
            self.session.redirect_uri = redirect_uri

        return(self.session.authorization_url(self._authorization_url, **kwargs))

    def fetch_access_token(self, code, redirect_uri=None):
        """Step 2: Given the code from Monzo from step 1, call
        Monzo again and returns an access token object. Extract the needed
        information from that and save it to use in future API calls.
        the token is internally saved

            :rtype: A Dictionary representation of the authentication status.
        """
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.fetch_token(
            self._access_token_url,
            username=self.client_id,
            password=self.client_secret,
            code=code)

    def refresh_token(self):
        """Step 3: obtains a new access_token from the the refresh token
        obtained in step 2. Only do the refresh if there is `token_updater(),`
        which saves the token.

            :rtype: A Dictionary representation of the authentication token.
        """
        token = self.session.refresh_token(
            self._refresh_token_url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
            )

        token.update({'client_secret': self.client_secret})

        if self.session.token_updater:
            self.session.token_updater(token)

        return token

    def validate_response(self, response):
        """Validate the response and raises any appropriate errors.
           https://docs.monzo.com/#errors

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
