"""A wrapper around the official Monzo API endpoints.

This module contains the class `Monzo` which represents a wrapper around
HTTP calls to Monzo's API endpoints.
"""
from .request import Request
from .errors import NoAccessTokenError
import json
import os


class Monzo(object):
    """
    The class representation of Monzo's API endpoints.

       Please note that functions without a reference to the official Monzo API
       docs page are convinence functions which are created - based on the official
       API functions - to make life easier for developers.

       e.g. `get_first_account` calls `get_account` and returns the first `account`
       object, if it exists.

       :param access_token: The access token to authorise API calls.
    """

    API_URL = 'https://api.monzo.com/'  #: (str): A representation of the current Monzo api url.

    def __init__(self, access_token=False):
        """Init Method."""
        if access_token:
            self.access_token = access_token
        else:
            self.access_token = os.environ.get('MONZO_ACCESS_TOKEN', None)

        if not self.access_token:
            raise(NoAccessTokenError)

        self.headers = {'Authorization': 'Bearer {0}'.format(self.access_token)}
        self.request = Request()
        self.who = self.whoami()

    def whoami(self):
        """
        Give information about an access token. (https://monzo.com/docs/#authenticating-requests).

        :rtype: A Dictionary representation of the authentication status.
        """
        url = "{0}/ping/whoami".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return WhoAmI(response)

    def get_accounts(self, **parameters):
        """
        Get all accounts that belong to a user. (https://monzo.com/docs/#list-accounts).

           :rtype: A Collection of accounts for a user.

        """
        url = "{0}/accounts".format(self.API_URL)
        response = self.request.get(url, headers=self.headers, params=parameters)

        return [Account(x) for x in response['accounts']]

    def get_current_account(self):
        """
        Get the first account for a user.

           :rtype: A Dictionary representation of the first account belonging to a user, if it exists.

        """
        accounts = self.get_accounts(account_type="uk_retail")
        if len(accounts) <= 0:
            raise LookupError('There are no accounts associated with this user.')
        return accounts[0]

    def get_pots(self, **parameters):
        """
        Get all accounts that belong to a user. (https://monzo.com/docs/#list-pots).

           :rtype: A Collection of pots for a user.

        """
        url = "{0}/pots".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)

        return [Pot(x) for x in response['pots'] if x['deleted'] != "true"]

    def get_first_account(self):
        """
        Get the first account for a user.

           :rtype: A Dictionary representation of the first account belonging to a user, if it exists.

        """
        accounts = self.get_accounts()
        if len(accounts) <= 0:
            raise LookupError('There are no accounts associated with this user.')
        return accounts[0]

    def get_transactions(self, **parameters):
        """
        Get all transactions of a given account. (https://monzo.com/docs/#list-transactions).

           :param account_id: The unique identifier for the account which the transactions belong to.
           :rtype: A collection of transaction objects for specific user.
        """
        url = "{0}/transactions".format(self.API_URL)
        params = {'expand[]': 'merchant', 'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return [Transaction(x) for x in response['transactions']]

    def get_balance(self, account_id):
        """
        Get the balance of a given account. (https://monzo.com/docs/#read-balance).

           :param account_id: The unique identifier for the account which the balance belong to.
           :rtype: Dictionary representation of the current account balance.

        """
        url = "{0}/balance".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return Balance(response)

    def get_webhooks(self, account_id):
        """
        Get the webhooks of a given account. (https://monzo.com/docs/#list-webhooks).

           :param account_id: The unique identifier for the account which the webhooks belong to.
           :rtype: A collection of webhooks that belong to an account.

        """
        url = "{0}/webhooks".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)

        return [WebHook(x) for x in response['webhooks']]

    def get_first_webhook(self, account_id):
        """
        Get the first webhook of a given account.

           :param account_id: The unique identifier for the account which the first webhook belong to.
           :rtype: A Dictionary representation of the first webhook belonging to an account, if it exists.
        """
        webhooks = self.get_webhooks(account_id)
        if len(webhooks) <= 0:
            raise LookupError('There are no webhooks associated with the account.')
        return webhooks[0]

    def delete_webhook(self, webhook_id):
        """
        Delete the a specified webhook. (https://monzo.com/docs/#deleting-a-webhook).

           :param webhook_id: The unique identifier for the webhook to delete.
           :rtype: An empty Dictionary, if the deletion was successful.
        """
        url = "{0}/webhooks/{1}".format(self.API_URL, webhook_id)
        response = self.request.delete(url, headers=self.headers)
        return response

    def delete_all_webhooks(self, account_id):
        """
        Remove all webhooks associated with the first account, if it exists.

           :rtype: None
        """
        webhooks = self.get_webhooks(account_id)
        for webhook in webhooks:
            self.delete_webhook(webhook.id)

    def register_webhook(self, webhook_url, account_id):
        """
        Register a webhook. (https://monzo.com/docs/#registering-a-webhook).

           :param webhook_url: The webhook url to register.
           :param account_id: The unique identifier for the account to register the webhook.

           :rtype: Registers a webhook to an account.
        """
        url = "{0}/webhooks".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'account_id': account_id, 'url': webhook_url})
        return response

    def register_attachment(self, transaction_id, file_url, file_type):
        """
        Attach an image to a transaction. (https://monzo.com/docs/#register-attachment).

           :param transaction_id: The unique identifier for the transaction to register the attachment to.
           :param file_url: The url of the file to attach.
           :param transaction_id: The type of the file specified in file_url

           :rtype: Dictionary representation of the attachment that was just registered.
        """
        url = "{0}/attachment/register".format(self.API_URL)
        response = self.request.post(
            url,
            headers=self.headers,
            data={
                'external_id': transaction_id,
                'file_url': file_url,
                'file_type': file_type
            }
        )
        return response

    def deregister_attachment(self, attachment_id):
        """
        Removed a previously attached image from a transaction. (https://monzo.com/docs/#deregister-attachment).

            :param transaction_id: The unique identifier for the attachment to deregister.
            :rtype: An empty Dictionary, if the deregistration was successful.
        """
        url = "{0}/attachment/deregister".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'id': attachment_id})
        return response

    def create_feed_item(self, account_id, feed_type, url, params):
        """
        Create a feed item. (https://monzo.com/docs/#create-feed-item).

            :param account_id: The unique identifier for the account to create the feed item for.
            :param feed_type: The type of feed item (currently only `basic` is supported).
            :param url: The url to open if a feed item is tapped
            :param params: A map of parameters which vary based on type

            :rtype: An empty Dictionary, if the feed item creation was successful.
        """
        url = "{0}/feed".format(self.API_URL)
        data = {
            'account_id': account_id,
            'type': feed_type,
            'url': url,
            "params[title]": params['title'],
            "params[image_url]": params['image_url'],
            "params[body]": params['body']
        }
        response = self.request.post(url,
                                     headers=self.headers,
                                     data=data
                                     )
        return response


class MonzoAPIObject(object):
    """MonzoAPiObject Uused to convert JSON response to Python Object."""

    def __init__(self, raw, attribute_map):
        """Init method of MonzoAPiObject."""
        self.raw = raw

        for attribute, value in attribute_map.items():
            if type(value) is str:
                setattr(self, attribute, raw.get(value, None))
            else:
                setattr(self, attribute, value)

    def to_json(self):
        """Return JSON of the raw input."""
        return json.dumps(self.raw)

    def convert_amount(self, to_convert):
        return "{:.2f}".format(
            round(float(to_convert) / 100, 2)
        )

class WebHook(MonzoAPIObject):

    def __init__(self, raw):
        super(WebHook, self).__init__(
            raw,
            {
                "id": "id",
                "url": "url",
                "account": "account_id"
            }
        )

class Address(MonzoAPIObject):

    def __init__(self, raw):
        super(Address, self).__init__(
            raw,
            {
                "address": "address",
                "city": "city",
                "country": "country",
                "latitude": "latitude",
                "longitude": "longitude",
                "postcode": "postcode",
                "region": "region"
            }
        )

class Merchant(MonzoAPIObject):

    def __init__(self, raw):
        super(Merchant, self).__init__(
            raw,
            {
                "created": "created",
                "group_id": "group_id",
                "id": "id",
                "logo": "logo",
                "emoji": "emoji",
                "name": "name",
                "category": "category"
            }
        )

        self.address = raw.get('address', None)
        if self.address:
            self.address = Address(raw)

class Transaction(MonzoAPIObject):

    def __init__(self, raw):
        super(Transaction, self).__init__(
            raw,
            {
                "account_balance": "account_balance",
                "amount": "amount",
                "created": "created",
                "currency": "currency",
                "description": "description",
                "id": "id",
                "notes": "notes",
                "settled": "settled"
            }
        )

        self.amount = self.convert_amount(self.amount)
        self.account_balance = self.convert_amount(self.account_balance)

        self.merchant = raw.get("merchant", None)
        if self.merchant:
            self.merchant = Merchant(raw)


class WhoAmI(MonzoAPIObject):
    """WhoAmI Object."""

    def __init__(self, raw):
        """Init Method."""
        super(WhoAmI, self).__init__(
            raw,
            {
                "id": "user_id",
                "client_id": "client_id",
                "authenticated": "authenticated"
            }
        )


class Account(MonzoAPIObject):
    """Monzo Account."""

    def __init__(self, raw):
        """Init Method."""
        super(Account, self).__init__(
            raw,
            {
                "id": "id",
                "closed": "closed",
                "created": "created",
                "account_type": "type",
                "description": "description",
                "account_number": "account_numebr",
                "sort_code": "sort_code"
            }
        )

        name_parts = self.description.split(" ")
        self.first_name = name_parts[0]
        self.last_name = name_parts[-1]

        if len(name_parts) > 2:
            self.middle_names = name_parts[1:-1]


class Pot(MonzoAPIObject):
    """Monzo Pot."""

    def __init__(self, raw):
        """Init Method."""
        super(Pot, self).__init__(
            raw,
            {
                "id": "id",
                "name": "name",
                "style": "style",
                "balance": "balance",
                "currency": "currency",
                "created": "created",
                "updated": "updated"
            }
        )

        self.balance = self.convert_amount(self.balance)


class Balance(MonzoAPIObject):
    """Balance class."""

    def __init__(self, raw):
        """Init Method."""
        super(Balance, self).__init__(
            raw,
            {
                "balance": "balance",
                "total_balance": "total_balance",
                "currency": "currency",
                "spend_today": "spend_today",
                "local_currency": "local_currency",
                "local_exchange_rate": "local_exchange_rate",
                "local_spend": "local_spend"
            }
        )

        self.balance = self.convert_amount(self.balance)

        self.total_balance = self.convert_amount(self.total_balance)

