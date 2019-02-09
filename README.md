[![Build Status](https://travis-ci.org/muyiwaolu/monzo-python.svg?branch=master)](https://travis-ci.org/muyiwaolu/monzo-python)
# monzo-python
This is a simple wrapper around the official Monzo API written in Python.

# Quickstart
Make sure you have Python and pip on your machine (this package was built and tested with Python >3.4, but it should work with 2.7, too. Your mileage may vary with other versions).

To install the package run

`pip install monzo`

If the above doesn’t work, you may want to run the above command as an admin by prefixing `sudo`.

# monzo-python in action
Open up a Python terminal (or create a Python file) and enter the following:

```python
from monzo import Monzo # Import Monzo class

client = Monzo('access_token_goes_here') # Replace access token with a valid token found at: https://developers.monzo.com/
account_id = client.get_first_account()['id'] # Get the ID of the first account linked to the access token
balance = client.get_balance(account_id) # Get your balance object
print(balance['balance']) # 100000000000
print(balance['currency']) # GBP
print(balance['spend_today']) # 2000
```

Yup. That easy. To see what more you can do with the client variable, take a look at the [tests](https://github.com/muyiwaolu/monzo-python/blob/master/tests/test_api_endpoints.py).

# Using monzo-python in an OAuth application

The access token given in the Monzo Developer Playground will expire after a short period of a few hours.
For applications integrating monzo-python which need access to the Monzo API for longer periods, you will need to use a OAuth session.

## Getting OAuth credentials

In order to get OAuth credentials for monzo-python:
1. Head to the [Clients Section](https://developers.monzo.com/apps/home) of the developer playground.
2. Click "New OAuth Client".
3. Give your client a name, e.g. "MyApplication".
4. Enter the "Redirect URL" as the URL on which MyApplication will listen for an authentication code.

   e.g. `http://[MyApplication URL]/api/monzo/callback`
5. Select "Confidential" from the Confidentiality dropdown box.
6. Click "Submit" and make a note of the newly created client id and secret, you will need this for your Home Assistant configuration.

Note: If your application doesn't include a http server which can pass the authentication code sent to the redirect url on to monzo-python, you can enter it as `http://localhost` and omit it from the following code.

## Getting an access token

To use a proper OAuth session in monzo-python we need to use the MonzoOAuth2Client class.

```python
from monzo import MonzoOAuth2Client # Import OAuth client class

oauth_client = MonzoOAuth2Client('client_id', 'client_secret',redirect_uri='redirect_url') # Replace with details entered on developer playground.

auth_start_url = oauth_client.authorize_token_url() # Returns a dictionary containing the Monzo authentication startpoint.
```

After authentication, Monzo will send the user an email containing a "magic link" to the redirect url you entered on the developer website. This url is appended with the authentication code which needs to be exchanged for an access token.

If your application includes a http server you may wish to add a handler to automatically pass the authentication code back to your `MonzoOAuth2Client`. Otherwise the user can extract the authentication code from the url and enter it manually.

```python3
oauth_client.fetch_access_token('authentication_code_from_magic_link')
```
At this point the OAuth session is complete and `oauth_client` will automatically refresh tokens as they expire.

To interact with the Monzo API we then insert our `oauth_client` into a `Monzo` object

```python3
from monzo import Monzo # Import Monzo class
client = Monzo.from_oauth_session(oauth_client)

```

By default the OAuth client token is automatically saved to the file `monzo.json`. If you want need to store this elsewhere in your application, this can be done by initialising `MonzoOAuth2Client` with the optional argument `refresh_callback` being the function handling updating token storage.
