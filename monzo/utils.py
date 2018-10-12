import datetime

def parse_transaction_datetimes(transaction):
    """Parse all timestamp strings in a transaction to datetime objects.

       :param transaction: A single transaction.
       :rtype: The transaction with datetimes parsed.
    """
    for (key, value) in transaction.items():
        try:
            time_string = value[:-1]
            time_components = time_string.split('.')
            time = datetime.datetime.strptime(time_components[0] , "%Y-%m-%dT%H:%M:%S")
            if len(time_components) > 1:
                time += datetime.timedelta(milliseconds=int(time_components[1].zfill(3)))
            transaction[key] = time
        except:
            if key in ('created', 'updated'):
                raise
            if key == 'settled' and value == '': # https://github.com/monzo/docs/pull/59
                continue
    return transaction

def parse_datetimes_for_all(transactions):
    """Parse timestamp strings in all transactions to datetime objects.

       :param transactions: The response from `get_transactions()`.
       :rtype: The transactions with datetimes parsed.
    """
    for transaction in transactions['transactions']:
        transaction = parse_transaction_datetimes(transaction)
    return transactions
 
