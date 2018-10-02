"""A data class representing a Monzo current account

This module contains the class `Account` which represents a prepaid or retail Monzo account
"""

class Account(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def __str__(self):
        string = ""
        keys = ['id', 'description', 'type', 'account_number', 'sort_code']
        for key in keys:
            string.append(key + ': ' + self[key] + '\n')
        string.append('open: ' + str(self.is_open()))
        return(string)

    def is_open(self):
        return(not self['closed'])

    def is_joint(self):
        return(len(self['owners']) > 1)

class Pot(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def __str__(self):
        string = ""
        keys = self.keys
        keys.remove('deleted')
        for key in keys:
            string.append(key + ': ' + self[key] + '\n')
        string.append('open: ' + str(self.is_open()))
        return(string)

    def is_open(self):
        return(not self['deleted'])

    def rounds_up_transactions(self):
        return(self['round_up'])

    def has_goal(self):
        return('goal_amount' in self.keys())
