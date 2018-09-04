"""A wrapper around the official Monzo API endpoints.

This module contains the class `Monzo` which represents a wrapper around
HTTP calls to Monzo's API endpoints.
"""
from monzo.request import Request
import string
import random

class Monzo(object):
    """The class representation of Monzo's API endpoints.

       Please note that functions without a reference to the official Monzo API
       docs page are convinence functions which are created - based on the official
       API functions - to make life easier for developers.

       e.g. `get_first_account` calls `get_account` and returns the first `account`
       object, if it exists.

       :param access_token: The access token to authorise API calls.
    """

    API_URL = 'https://api.monzo.com/' #: (str): A representation of the current Monzo api url.

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer {0}'.format(self.access_token)}
        self.request = Request()

    def whoami(self):
        """Gives information about an access token. (https://monzo.com/docs/#authenticating-requests)

           :rtype: A Dictionary representation of the authentication status.
        """
        url = "{0}/ping/whoami".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return response

    def get_accounts(self):
        """Get all accounts that belong to a user. (https://monzo.com/docs/#list-accounts)

           :rtype: A Collection of accounts for a user.

        """
        url = "{0}/accounts".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return response

    def get_first_account(self):
        """Gets the first account for a user.

           :rtype: A Dictionary representation of the first account belonging to a user, if it exists.

        """
        accounts = self.get_accounts()
        if len(accounts['accounts']) <= 0:
            raise LookupError('There are no accounts associated with this user.')
        return accounts['accounts'][0]

    def get_transactions(self, account_id):
        """Get all transactions of a given account. (https://monzo.com/docs/#list-transactions)

           :param account_id: The unique identifier for the account which the transactions belong to.
           :rtype: A collection of transaction objects for specific user.
        """
        url = "{0}/transactions".format(self.API_URL)
        params = {'expand[]': 'merchant', 'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_balance(self, account_id):
        """Gets the balance of a given account. (https://monzo.com/docs/#read-balance)

           :param account_id: The unique identifier for the account which the balance belong to.
           :rtype: Dictionary representation of the current account balance.

        """
        url = "{0}/balance".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_webhooks(self, account_id):
        """Gets the webhooks of a given account. (https://monzo.com/docs/#list-webhooks)

           :param account_id: The unique identifier for the account which the webhooks belong to.
           :rtype: A collection of webhooks that belong to an account.

        """
        url = "{0}/webhooks".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_first_webhook(self, account_id):
        """Gets the first webhook of a given account.

           :param account_id: The unique identifier for the account which the first webhook belong to.
           :rtype: A Dictionary representation of the first webhook belonging to an account, if it exists.
        """
        webhooks = self.get_webhooks(account_id)
        if len(webhooks['webhooks']) <= 0:
            raise LookupError('There are no webhooks associated with the account.')
        return webhooks['webhooks'][0]

    def delete_webhook(self, webhook_id):
        """Deletes the a specified webhook. (https://monzo.com/docs/#deleting-a-webhook)

           :param webhook_id: The unique identifier for the webhook to delete.
           :rtype: An empty Dictionary, if the deletion was successful.
        """
        url = "{0}/webhooks/{1}".format(self.API_URL, webhook_id)
        response = self.request.delete(url, headers=self.headers)
        return response

    def delete_all_webhooks(self):
        """Removes all webhooks associated with the first account, if it exists.

           :rtype: None
        """
        first_account = self.get_first_account()
        account_id = first_account['id']
        webhooks = self.get_webhooks(account_id)
        for webhook in webhooks['webhooks']:
            self.delete_webhook(webhook['id'])

    def register_webhook(self, webhook_url, account_id):
        """Registers a webhook. (https://monzo.com/docs/#registering-a-webhook)

           :param webhook_url: The webhook url to register.
           :param account_id: The unique identifier for the account to register the webhook.

           :rtype: Registers a webhook to an account.
        """
        url = "{0}/webhooks".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'account_id': account_id, 'url': webhook_url})

    def register_attachment(self, transaction_id, file_url, file_type):
        """Attaches an image to a transaction. (https://monzo.com/docs/#register-attachment)

           :param transaction_id: The unique identifier for the transaction to register the attachment to.
           :param file_url: The url of the file to attach.
           :param transaction_id: The type of the file specified in file_url

           :rtype: Dictionary representation of the attachment that was just registered.
        """
        url = "{0}/attachment/register".format(self.API_URL)
        response = self.request.post(url,
                                    headers=self.headers,
                                    data={'external_id': transaction_id,
                                          'file_url': file_url,
                                          'file_type': file_type})
        return response

    def deregister_attachment(self, attachment_id):
        """Removed a previously attached image from a transaction. (https://monzo.com/docs/#deregister-attachment)

            :param transaction_id: The unique identifier for the attachment to deregister.
            :rtype: An empty Dictionary, if the deregistration was successful.
        """
        url = "{0}/attachment/deregister".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'id': attachment_id})
        return response


    def create_feed_item(self, account_id, feed_type, url, params):
        """Creates a feed item. (https://monzo.com/docs/#create-feed-item)

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


    def get_pots(self):
        """Get all pots for a user. (https://monzo.com/docs/#list-pots)

           :rtype: A collection of pots for a user.

        """
        url = "{0}/pots".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return response


    def deposit_into_pot(self, pot_id, account_id, amount_in_pennies):
        """Move money from an account into a pot. (https://monzo.com/docs/#deposit-into-a-pot)

            :param pot_id: The unique identifier for the pot to deposit the money to.
            :param account_id: The unique identifier for the account to move the money from.
            :param amount_in_pennies: The amount of money to move to the pot in pennies.

            :rtype: A dictionary containing information on the pot that was updated.
        """
        url = "{0}/pots/{1}/deposit".format(self.API_URL, pot_id)
        unique_string = ''.join(random.choice(string.ascii_letters) for i in range(15))
        data = {
            'source_account_id': account_id,
            'amount': amount_in_pennies,
            'dedupe_id': unique_string
        }

        response = self.request.put(url, headers=self.headers, data=data)
        return response

    def withdraw_from_pot(self, account_id, pot_id, amount_in_pennies):
        """Move money from an account into a pot. (https://monzo.com/docs/#withdraw-from-a-pot)

            :param account_id: The unique identifier for the account to move the money to.
            :param pot_id: The unique identifier for the pot to withdraw the money from.
            :param amount_in_pennies: The amount of money to move to the pot in pennies.

            :rtype: A dictionary containing information on the pot that was updated.
        """
        url = "{0}/pots/{1}/withdraw".format(self.API_URL, pot_id)
        unique_string = ''.join(random.choice(string.ascii_letters) for i in range(15))
        data = {
            'destination_account_id': account_id,
            'amount': amount_in_pennies,
            'dedupe_id': unique_string
        }

        response = self.request.put(url, headers=self.headers, data=data)
        return response

