from monzo.monzo import Monzo
from settings import get_environment_var

client = Monzo(get_environment_var('ACCESS_TOKEN'))
account_id = client.get_first_account()['id']
transactions = client.get_transactions(account_id)['transactions']
for transaction in transactions:
     if transaction['attachments']:
         for attachment in transaction['attachments']:
            client.deregister_attachment(attachment['id'])
