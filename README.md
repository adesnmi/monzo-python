[![Build Status](https://travis-ci.org/muyiwaolu/monzo-python.svg?branch=master)](https://travis-ci.org/muyiwaolu/monzo-python)
# monzo-python
This is a simple wrapper around the official Monzo API written in Python.

# Quickstart
Make sure you have Python and pip on your machine (this package was built and tested with Python 3.5, but it should work with 2.7, too. Your mileage may vary with other versions).

To install the package run

`pip install monzo`

If the above doesn’t work, you may want to run the above command as an admin by prefixing `sudo`.

# Monzo Python in action
Open up a Python terminal (or create a Python file) and enter the following:

```
from monzo.monzo import Monzo # Import Monzo Class

client = Monzo('access_token_goes_here') # Replace access token with a valid token found at: https://developers.getmondo.co.uk/
account_id = client.get_first_account()['id'] # Get the ID of the first account linked to the access token
balance = client.get_balance(account_id) # Get your balance object
print(balance['balance']) # 100000000000
print(balance['currency']) # GBP
print(balance['spend_today']) # 2000
```

Yup. That easy. To see what more you can do with the client variable, take a look at the [tests](https://github.com/muyiwaolu/monzo-python/blob/master/tests/test_api_endpoints.py).
