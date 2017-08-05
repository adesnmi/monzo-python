"""A replacement for monzo.monzo.Monzo for testing puropses
"""

class Monzo(object):
    """The stubbed out class representation of the Monzo client
    """

    def __init__(self, access_token):
        pass

    def whoami(self):
        """Gives information about an access token.
           (https://monzo.com/docs/#authenticating-requests)

           :rtype: A stubbed dictionary representation of the authentication status.
        """
        return {
            "authenticated": True,
            "client_id": "client_id",
            "user_id": "user_id"
        }

    def get_accounts(self):
        """Get all accounts that belong to a user. (https://monzo.com/docs/#list-accounts)

           :rtype: A stubbed collection of accounts for a user.

        """
        return {
            "accounts": [
                {
                    "id": "acc_00009237aqC8c5umZmrRdh",
                    "description": "Peter Pan's Account",
                    "created": "2015-11-13T12:17:42Z"
                }
            ]
        }

    def get_first_account(self):
        """Gets the first account for a user.

           :rtype: A stubbed dictionary representation of the authentication status.

        """
        accounts = self.get_accounts()
        return accounts['accounts'][0]

    def get_transactions(self, account_id):
        """Get all transactions of a given account. (https://monzo.com/docs/#list-transactions)

           :param account_id: The unique identifier for the account which the transactions belong to.
           :rtype: A stubbed collection of transaction objects for specific user.
        """
        return {
            "transactions": [
                {
                    "account_balance": 13013,
                    "amount": -510,
                    "created": "2015-08-22T12:20:18Z",
                    "currency": "GBP",
                    "description": "THE DE BEAUVOIR DELI C LONDON        GBR",
                    "id": "tx_00008zIcpb1TB4yeIFXMzx",
                    "merchant": "merch_00008zIcpbAKe8shBxXUtl",
                    "metadata": {},
                    "notes": "Salmon sandwich 🍞",
                    "is_load": False,
                    "settled": "2015-08-23T12:20:18Z",
                    "category": "eating_out"
                },
                {
                    "account_balance": 12334,
                    "amount": -679,
                    "created": "2015-08-23T16:15:03Z",
                    "currency": "GBP",
                    "description": "VUE BSL LTD            ISLINGTON     GBR",
                    "id": "tx_00008zL2INM3xZ41THuRF3",
                    "merchant": "merch_00008z6uFVhVBcaZzSQwCX",
                    "metadata": {},
                    "notes": "",
                    "is_load": False,
                    "settled": "2015-08-24T16:15:03Z",
                    "category": "eating_out"
                },
            ]
        }

    def get_balance(self, account_id):
        """Gets the balance of a given account. (https://monzo.com/docs/#read-balance)

           :param account_id: The unique identifier for the account which the balance belong to.
           :rtype: A stubbed dictionary representation of the current account balance.

        """
        return {
            "balance": 5000,
            "currency": "GBP",
            "spend_today": 0
        }

    def get_webhooks(self, account_id):
        """Gets the webhooks of a given account. (https://monzo.com/docs/#list-webhooks)

           :param account_id: The unique identifier for the account which the webhooks belong to.
           :rtype: A stubbed collection of webhooks that belong to an account.

        """
        return {
            "webhooks": [
                {
                    "account_id": "acc_000091yf79yMwNaZHhHGzp",
                    "id": "webhook_000091yhhOmrXQaVZ1Irsv",
                    "url": "http://example.com/callback"
                },
                {
                    "account_id": "acc_000091yf79yMwNaZHhHGzp",
                    "id": "webhook_000091yhhzvJSxLYGAceC9",
                    "url": "http://example2.com/anothercallback"
                }
            ]
        }

    def get_first_webhook(self, account_id):
        """Gets the first webhook of a given account.

           :param account_id: The unique identifier for the account which the first webhook belong to.
           :rtype: A stubbed dictionary representation of the first webhook belonging to an account, if it exists.
        """
        webhooks = self.get_webhooks(account_id)
        return webhooks['webhooks'][0]

    def delete_webhook(self, webhook_id):
        """Deletes the a specified webhook. (https://monzo.com/docs/#deleting-a-webhook)

           :param webhook_id: The unique identifier for the webhook to delete.
           :rtype: An empty dictionary
        """
        return {}

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

           :rtype: A stubbed dictionary representing a webhook 
        """
        return {
            "webhook": {
                "account_id": "account_id",
                "id": "webhook_id",
                "url": "http://example.com"
            }
        }

    def register_attachment(self, transaction_id, file_url, file_type):
        """Attaches an image to a transaction. (https://monzo.com/docs/#register-attachment)

           :param transaction_id: The unique identifier for the transaction to register the attachment to.
           :param file_url: The url of the file to attach.
           :param transaction_id: The type of the file specified in file_url

           :rtype: A stubbed dictionary representation of the attachment that was just registered.
        """
        return {
            "attachment": {
                "id": "attach_00009238aOAIvVqfb9LrZh",
                "user_id": "user_00009238aMBIIrS5Rdncq9",
                "external_id": "tx_00008zIcpb1TB4yeIFXMzx",
                "file_url": "https://s3-eu-west-1.amazonaws.com/mondo-image-uploads/user_00009237hliZellUicKuG1/LcCu4ogv1xW28OCcvOTL-foo.png",
                "file_type": "image/png",
                "created": "2015-11-12T18:37:02Z"
            }
        }

    def deregister_attachment(self, attachment_id):
        """Removed a previously attached image from a transaction. (https://monzo.com/docs/#deregister-attachment)

            :param transaction_id: The unique identifier for the attachment to deregister.
            :rtype: An empty Dictionary, if the deregistration was successful.
        """
        return {}


    def create_feed_item(self, account_id, feed_type, url, params):
        """Creates a feed item. (https://monzo.com/docs/#create-feed-item)

            :param account_id: The unique identifier for the account to create the feed item for.
            :param feed_type: The type of feed item (currently only `basic` is supported).
            :param url: The url to open if a feed item is tapped
            :param params: A map of parameters which vary based on type

            :rtype: An empty Dictionary, if the feed item creation was successful.
        """
        return {}
