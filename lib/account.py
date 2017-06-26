import logging
from decimal import Decimal

class Account (object):

    def add (self, amount):
        amount = Decimal (amount)
        logging.info ('adding {} to {}'.format (amount, self.name))
        self.balance += amount

    def sub (self, amount):
        amount = Decimal (amount)
        if self.balance < amount:
            raise UserWarning ('balance too small')

        logging.info ('subtracting {} from {}'.format (amount, self.name))
        self.balance -= amount

    @property
    def balance (self):
        return self._balance

    @balance.setter
    def balance (self, v):
        v = Decimal (v)
        logging.info ('setting balance of {} to {}'.format (self.name, v))
        self._balance = v
