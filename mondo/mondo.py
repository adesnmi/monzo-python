"""A wrapper around the official Mondo API endpoints."""
import datetime
import requests

class Mondo(object):
    """The class representation of Mondo's API endpoints."""
    API_URL = 'https://api.getmondo.co.uk/'
    def __init__(self, access_token):
        self.access_token = access_token

    def whoami(self):
        """Gives information about an access token."""
        url = "{0}/ping/whoami".format(self.API_URL)
        headers = {'Authorization': 'Bearer {0}'.format(self.access_token)}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_accounts(self):
        """Get all accounts that belong to a user."""
        raise NotImplementedError()

    def get_transactions(self, account_id):
        """Get all transactions of a given account."""
        raise NotImplementedError()

    def get_balance(self, account_id):
        """Gets the balance of a given account."""
        raise NotImplementedError()

    def get_webhooks(self, account_id):
        """Gets the webhooks of a given account."""
        raise NotImplementedError()

    def delete_webhook(self, webhook_id):
        """Deletes the a specified webhook."""
        raise NotImplementedError()

    def register_webhook(self, url):
        """Registers a webhook."""
        raise NotImplementedError()

    def attach_image_to_transaction(self, file_url, file_type):
        """Attaches an image to a transaction."""
        raise NotImplementedError()

    def create_feed_item(self, account_id, feed_type, url, params):
        """Creates a feed item."""
        raise NotImplementedError()
