import datetime

def parse_datetimes(transactions):
    """Parse timestamp strings to datetime objects.

       :param transactions: The response from `get_transactions`.
       :rtype: The collection of transaction objects with datetimes parsed.
    """
    for txn in transactions['transactions']:
        for (key, value) in txn.items():
            try:
                time_string = value[:-1]
                time_components = time_string.split('.')
                time = datetime.datetime.strptime(time_components[0] , "%Y-%m-%dT%H:%M:%S")
                if len(time_components) > 1:
                    time += datetime.timedelta(milliseconds=int(time_components[1].zfill(3)))
                txn[key] = time
            except:
                if key in ('created', 'updated'):
                    raise
                if key == 'settled' and value == '': # https://github.com/monzo/docs/pull/59
                    continue
    return transactions
