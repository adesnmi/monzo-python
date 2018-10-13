"""A data class representing a Monzo current account

This module contains the class `Account` which represents a prepaid or retail Monzo account
"""

class Account(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def is_open(self):
        return(not self['closed'])

    def is_joint(self):
        return(len(self['owners']) > 1)

class Pot(dict):

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, dict(self))

    def is_open(self):
        return(not self['deleted'])

    def rounds_up_transactions(self):
        return(self['round_up'])

    def has_goal(self):
        return('goal_amount' in self.keys())

    def reached_goal(self):
        return(self['goal_amount'] <= self['balance'])
