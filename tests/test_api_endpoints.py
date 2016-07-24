from mondo.mondo import Mondo
from settings import get_environment_var
import pytest

class TestApiEndpoints:
    @pytest.fixture
    def client(self):
        return Mondo(get_environment_var('ACCESS_TOKEN'))

    def test_whoami(self, client):
        whoami = client.whoami()
        assert whoami['authenticated']

    def test_get_accounts(self, client):
        with pytest.raises(NotImplementedError):
            client.get_accounts()

    def test_get_transactions(self, client):
        with pytest.raises(NotImplementedError):
            client.get_transactions(account_id=1)

    def test_get_balance(self, client):
        with pytest.raises(NotImplementedError):
            client.get_balance(account_id=1)

    def test_get_webhooks(self, client):
        with pytest.raises(NotImplementedError):
            client.get_webhooks(account_id=1)

    def test_delete_webhook(self, client):
        with pytest.raises(NotImplementedError):
            client.delete_webhook(webhook_id=1)

    def test_register_webhook(self, client):
        with pytest.raises(NotImplementedError):
            client.register_webhook(url='https://google.co.uk')

    def test_attach_image_to_transaction(self, client):
        with pytest.raises(NotImplementedError):
            client.attach_image_to_transaction(file_url='test', file_type='test')

    def test_create_feed_item(self, client):
        with pytest.raises(NotImplementedError):
            client.create_feed_item(account_id=1, feed_type='basic',
                                    url='https://google.co.uk', params=[])
