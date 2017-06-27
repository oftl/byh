import logger
from decimal import Decimal

class Account (logger.Logger):

    def add (self, amount):
        amount = Decimal (amount)
        self.logger.info ('adding {} to {}'.format (amount, self.name))
        self.balance += amount

    def sub (self, amount):
        amount = Decimal (amount)
        if self.balance < amount:
            raise UserWarning ('balance too small')

        self.logger.info ('subtracting {} from {}'.format (amount, self.name))
        self.balance -= amount

    @property
    def balance (self):
        return self._balance

    @balance.setter
    def balance (self, v):
        v = Decimal (v)
        self.logger.info ('setting balance of {} to {}'.format (self.name, v))
        self._balance = v
