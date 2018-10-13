"""A data class representing a Monzo current account

This module contains the class `Account` which represents a prepaid or retail Monzo account
"""

class Transaction(dict):

    def __init__(self, dict_rep):
        print(dict_rep)
        if dict_rep['merchant'] is not None:
            dict_rep['merchant'] = Merchant(dict_rep['merchant'])
        super().__init__(dict_rep)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def can_split_bill(self):
        return(self['can_split_the_bill'])


class TransactionList(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def nextpage(self):
        """ """
        if 'next_page' in self:
            return self['next_page']()


class Merchant(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))
