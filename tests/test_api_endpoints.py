import pytest
from doubles.monzo import Monzo

class TestApiEndpoints:
    @pytest.fixture
    def client(self):
        return Monzo('stubbed')

    # def test_whoami(self, client):
    #     whoami = client.whoami()
    #     assert whoami['authenticated']
    #
    # def test_get_accounts(self, client):
    #     accounts = client.get_accounts()
    #     assert accounts['accounts'] is not None
    #
    # def test_get_transactions(self, client):
    #     account_id = client.get_first_account()['id']
    #     transactions = client.get_transactions(account_id)
    #     assert transactions['transactions'] is not None
    #
    # def test_get_balance(self, client):
    #     account_id = client.get_first_account()['id']
    #     balance = client.get_balance(account_id)
    #     assert balance['balance'] is not None
    #
    # def test_get_webhooks(self, client):
    #     account_id = client.get_first_account()['id']
    #     webhooks = client.get_webhooks(account_id)
    #     assert webhooks['webhooks'] is not None
    #
    # def test_delete_webhook(self, client):
    #     account_id = client.get_first_account()['id']
    #     client.register_webhook(webhook_url='https://google.co.uk', account_id=account_id)
    #     webhooks = client.get_webhooks(account_id)
    #     webhook_count = len(webhooks['webhooks'])
    #     webhook_id = client.get_first_webhook(account_id)['id']
    #     client.delete_webhook(webhook_id)
    #     new_webhooks = client.get_webhooks(account_id)
    #     new_webhooks_count = len(new_webhooks['webhooks'])
    #     assert new_webhooks_count == webhook_count - 1
    #     client.delete_all_webhooks()
    #
    # def test_register_webhook(self, client):
    #     account_id = client.get_first_account()['id']
    #     client.register_webhook(webhook_url='https://google.co.uk', account_id=account_id)
    #     webhooks = client.get_webhooks(account_id)
    #     webhook_in_webhooks = [w for w in webhooks['webhooks'] if w['url'] == 'https://google.co.uk']
    #     assert len(webhook_in_webhooks) > 0
    #     client.delete_all_webhooks()
    #
    #
    # def test_register_and_remove_attachment(self, client):
    #     account_id = client.get_first_account()['id']
    #     transactions = client.get_transactions(account_id)
    #     first_transaction_id = transactions['transactions'][0]['id']
    #     image_attachment = client.register_attachment(transaction_id=first_transaction_id,
    #                                        file_url='http://www.nyan.cat/cats/original.gif',
    #                                        file_type='image/gif')
    #     attachment_id = image_attachment['attachment']['id']
    #     assert attachment_id is not None
    #     deregistered_attachment_response = client.deregister_attachment(attachment_id)
    #     assert deregistered_attachment_response is not None
    #
    #
    # def test_create_feed_item(self, client):
    #     account_id = client.get_first_account()['id']
    #     params = {'title': 'Python Testing :D',
    #               'body': 'Is this real life?',
    #               'image_url': 'http://www.nyan.cat/cats/original.gif'}
    #     feed_item = client.create_feed_item(account_id=account_id,
    #                                         feed_type='basic',
    #                                         url='http://www.nyan.cat/',
    #                                         params=params)
    #     assert feed_item is not None
