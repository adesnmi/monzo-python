"""A data class representing a Monzo current account balance

This module contains the class `Balance` which represents a prepaid or retail Monzo account
"""

class Balance(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def spending_nonstandard_currency(self):
        return(self['local_currency'] != self['currency'] and self['local_currency'] != '')

    def exhange_rate_to_local_currency(self):
        # Can't complete this as I can't see how it is displayed in API
        # Depending on this, the implementations of these methods may be switched

        # return(self['local_exchange_rate'])
        raise NotImplementedError

    def exhange_rate_from_local_currency(self):
        # return(1/self['local_exchange_rate'])
        raise NotImplementedError
