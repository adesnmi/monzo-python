# This project is no longer under active development

It's been a while since I've written Python as my primary language, not to mention life and work doesn't allow me to spend enough time on this project. Please feel free to fork and continue the work. As for the `monzo` namespace for `PyPy`, I'll be keeping a hold of it for security reasons.

[![CircleCI](https://circleci.com/gh/muyiwaolu/monzo-python/tree/dev.svg?style=svg)](https://circleci.com/gh/muyiwaolu/monzo-python/tree/dev)
# monzo-python

## Requirements

* `Python >= 3.5`

## Quickstart
Make sure you have Python and pip on your machine

To install the package run

`pip install monzo`

If the above doesn’t work, you may want to run the above command as an admin by prefixing `sudo`.

### Example
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

Yup. That easy. To see what more you can do with the `client` variable, take a look at the [tests](https://github.com/muyiwaolu/monzo-python/blob/master/tests/test_api_endpoints.py).

### OAuth

The library also supports OAuth. Read the [wiki entry](https://github.com/muyiwaolu/monzo-python/wiki/OAuth) for more information.
