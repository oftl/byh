class Account (object):

    def add (self, amount):
        self.balance += amount

    def sub (self, amount):
        if self.balance < amount:
            raise UserWarning ('balance too small')

        self.balance -= amount

    @property
    def balance (self):
        return self._balance

    @balance.setter
    def balance (self, v):
        self._balance = v
