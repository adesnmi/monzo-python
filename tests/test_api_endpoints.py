import pytest
from doubles.monzo import Monzo


class TestApiEndpoints:
    @pytest.fixture
    def client(self):
        return Monzo("stubbed")

    def test_whoami(self, client):
        whoami = client.whoami()
        assert whoami["authenticated"]

    def test_get_accounts(self, client):
        accounts = client.get_accounts()
        assert accounts["accounts"] is not None

    def test_get_transactions(self, client):
        account_id = client.get_first_account()["id"]
        transactions = client.get_transactions(account_id)
        assert transactions["transactions"] is not None

    def test_get_transaction(self, client):
        account_id = client.get_first_account()["id"]
        first_transaction_id = client.get_transactions(account_id)["transactions"][0][
            "id"
        ]
        transaction_data = client.get_transaction(first_transaction_id)
        assert transaction_data["transaction"] is not None

    def test_get_balance(self, client):
        account_id = client.get_first_account()["id"]
        balance = client.get_balance(account_id)
        assert balance["balance"] is not None

    def test_get_pots(self, client):
        pots = client.get_pots()["pots"]
        assert pots is not None

    def test_deposit_into_pot(self, client):
        pot_id = client.get_pots()["pots"][0]["id"]
        account_id = client.get_first_account()["id"]
        pot_info = client.deposit_into_pot(pot_id, account_id, 1000)
        assert pot_info is not None

    def test_withdraw_from_pot(self, client):
        pot_id = client.get_pots()["pots"][0]["id"]
        account_id = client.get_first_account()["id"]
        pot_info = client.withdraw_from_pot(account_id, pot_id, 1000)
        assert pot_info is not None

    def test_get_webhooks(self, client):
        account_id = client.get_first_account()["id"]
        webhooks = client.get_webhooks(account_id)
        assert webhooks["webhooks"] is not None

    def test_delete_webhook(self, client):
        account_id = client.get_first_account()["id"]
        client.register_webhook(
            webhook_url="https://google.co.uk", account_id=account_id
        )
        webhook_id = client.get_first_webhook(account_id)["id"]
        assert client.delete_webhook(webhook_id) == {}

    def test_register_webhook(self, client):
        account_id = client.get_first_account()["id"]
        client.register_webhook(
            webhook_url="https://google.co.uk", account_id=account_id
        )
        webhooks = client.get_webhooks(account_id)
        assert len(webhooks) > 0

    def test_register_and_remove_attachment(self, client):
        account_id = client.get_first_account()["id"]
        transactions = client.get_transactions(account_id)
        first_transaction_id = transactions["transactions"][0]["id"]
        image_attachment = client.register_attachment(
            transaction_id=first_transaction_id,
            file_url="does not matter",
            file_type="does not matter",
        )
        attachment_id = image_attachment["attachment"]["id"]
        assert attachment_id is not None
        deregistered_attachment_response = client.deregister_attachment(attachment_id)
        assert deregistered_attachment_response is not None

    def test_create_feed_item(self, client):
        account_id = client.get_first_account()["id"]
        params = {
            "title": "does not matter",
            "body": "does not matter",
            "image_url": "does not matter",
        }
        feed_item = client.create_feed_item(
            account_id=account_id, feed_type="blah", url="blah", params=params
        )
        assert feed_item is not None

    def test_update_transaction_metadata(self, client):
        account_id = client.get_first_account()["id"]
        transactions = client.get_transactions(account_id)
        first_transaction_id = transactions["transactions"][0]["id"]
        updated_transaction = client.update_transaction_metadata(
            transaction_id=first_transaction_id, key="keyvalue", value="does not matter"
        )
        assert updated_transaction is not None
