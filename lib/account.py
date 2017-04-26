import logging

class Account (object):

    def add (self, amount):
        logging.info ('adding {} to {}'.format (amount, self.name))
        self.balance += amount

    def sub (self, amount):
        if self.balance < amount:
            raise UserWarning ('balance too small')

        logging.info ('subtracting {} from {}'.format (amount, self.name))
        self.balance -= amount

    @property
    def balance (self):
        return self._balance

    @balance.setter
    def balance (self, v):
        self._balance = v
