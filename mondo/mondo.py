"""A wrapper around the official Mondo API endpoints."""
import datetime
import requests

class Mondo(object):
    """The class representation of Mondo's API endpoints."""
    API_URL = 'https://api.getmondo.co.uk/'
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer {0}'.format(self.access_token)}

    def whoami(self):
        """Gives information about an access token."""
        url = "{0}/ping/whoami".format(self.API_URL)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_accounts(self):
        """Get all accounts that belong to a user."""
        url = "{0}/accounts".format(self.API_URL)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_first_account(self):
        """Gets the first account for a user."""
        accounts = self.get_accounts()
        if len(accounts['accounts']) <= 0:
            raise LookupError('There are no accounts associated with this user.')
        return accounts['accounts'][0]

    def get_transactions(self, account_id):
        """Get all transactions of a given account."""
        url = "{0}/transactions?expand[]=merchant&account_id={1}".format(
                                                                    self.API_URL,
                                                                    account_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_balance(self, account_id):
        """Gets the balance of a given account."""
        url = "{0}/balance?account_id={1}".format(self.API_URL, account_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_webhooks(self, account_id):
        """Gets the webhooks of a given account."""
        url = "{0}/webhooks?account_id={1}".format(self.API_URL, account_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_first_webhook(self, account_id):
        """Gets the first webhook of a given account."""
        webhooks = self.get_webhooks(account_id)
        if len(webhooks['webhooks']) <= 0:
            raise LookupError('There are no webhooks associated with the account.')
        return webhooks['webhooks'][0]

    def delete_webhook(self, webhook_id):
        """Deletes the a specified webhook."""
        url = "{0}/webhooks/{1}".format(self.API_URL, webhook_id)
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def delete_all_webhooks(self):
        first_account = self.get_first_account()
        account_id = first_account['id']
        webhooks = self.get_webhooks(account_id)
        for webhook in webhooks['webhooks']:
            self.delete_webhook(webhook['id'])

    def register_webhook(self, webhook_url, account_id):
        """Registers a webhook."""
        url = "{0}/webhooks".format(self.API_URL)
        response = requests.post(url, headers=self.headers, data={'account_id': account_id, 'url': webhook_url})

    def attach_image_to_transaction(self, file_url, file_type):
        """Attaches an image to a transaction."""
        raise NotImplementedError()

    def create_feed_item(self, account_id, feed_type, url, params):
        """Creates a feed item."""
        raise NotImplementedError()
