Monzo Python
============

Monzo Python allows you to quickly and simply access, manipulate and
play with our banking data. Let's get started.

To install the package run (this package was built and tested with Python 3.5, your mileage
may vary with other versions) ::

    pip install mondo-python

Once you're done, open up a Python terminal (or create a Python file) and enter the following::

    from mondo.mondo import Mondo # Import Mondo Class

    client = Mondo('access_token_goes_here') # Replace access token with a valid token found at: https://developers.getmondo.co.uk/
    account_id = client.get_first_account()['id'] # Get the ID of the first account linked to the access token
    balance = client.get_balance(account_id) # Get your balance object
    print balance['balance'] # 100000000000
    print balance['currency'] # GBP
    print balance['spend_today'] # 2000

Yup. That easy. To see what more you can do with the `client` variable, take a look at the `Mondo Module` section
of the API docs linked below.


API DOCS
=========

.. toctree::
   :maxdepth: 4

   mondo

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
