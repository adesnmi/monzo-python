"""A wrapper around the official Mondo API endpoints."""
from .request import Request

class Mondo(object):
    """The class representation of Mondo's API endpoints."""
    API_URL = 'https://api.getmondo.co.uk/'
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer {0}'.format(self.access_token)}
        self.request = Request()

    def whoami(self):
        """Gives information about an access token."""
        url = "{0}/ping/whoami".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return response

    def get_accounts(self):
        """Get all accounts that belong to a user."""
        url = "{0}/accounts".format(self.API_URL)
        response = self.request.get(url, headers=self.headers)
        return response

    def get_first_account(self):
        """Gets the first account for a user."""
        accounts = self.get_accounts()
        if len(accounts['accounts']) <= 0:
            raise LookupError('There are no accounts associated with this user.')
        return accounts['accounts'][0]

    def get_transactions(self, account_id):
        """Get all transactions of a given account."""
        url = "{0}/transactions".format(self.API_URL)
        params = {'expand[]': 'merchant', 'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_balance(self, account_id):
        """Gets the balance of a given account."""
        url = "{0}/balance".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_webhooks(self, account_id):
        """Gets the webhooks of a given account."""
        url = "{0}/webhooks".format(self.API_URL)
        params = {'account_id': account_id}
        response = self.request.get(url, headers=self.headers, params=params)
        return response

    def get_first_webhook(self, account_id):
        """Gets the first webhook of a given account."""
        webhooks = self.get_webhooks(account_id)
        if len(webhooks['webhooks']) <= 0:
            raise LookupError('There are no webhooks associated with the account.')
        return webhooks['webhooks'][0]

    def delete_webhook(self, webhook_id):
        """Deletes the a specified webhook."""
        url = "{0}/webhooks/{1}".format(self.API_URL, webhook_id)
        response = self.request.delete(url, headers=self.headers)
        return response

    def delete_all_webhooks(self):
        first_account = self.get_first_account()
        account_id = first_account['id']
        webhooks = self.get_webhooks(account_id)
        for webhook in webhooks['webhooks']:
            self.delete_webhook(webhook['id'])

    def register_webhook(self, webhook_url, account_id):
        """Registers a webhook."""
        url = "{0}/webhooks".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'account_id': account_id, 'url': webhook_url})

    def register_attachment(self, transaction_id, file_url, file_type):
        """Attaches an image to a transaction."""
        url = "{0}/attachment/register".format(self.API_URL)
        response = self.request.post(url,
                                    headers=self.headers,
                                    data={'external_id': transaction_id,
                                          'file_url': file_url,
                                          'file_type': file_type})
        return response

    def deregister_attachment(self, attachment_id):
        """Removed a previously attached image from a transaction."""
        url = "{0}/attachment/deregister".format(self.API_URL)
        response = self.request.post(url, headers=self.headers, data={'id': attachment_id})
        return response


    def create_feed_item(self, account_id, feed_type, url, params):
        """Creates a feed item."""
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
