from decimal import Decimal as D

import lib.byh

class Outcome (lib.byh.Byh):

    def __init__ (self, **kwa):
        self._id    = kwa.get ('id')
        self._new   = kwa.get ('_new')
        self._text  = kwa.get ('text')
        self._odds  = kwa.get ('odds')
        self._winner = kwa.get ('winner')
        self._db    = kwa.get ('db')

    def __repr__ (self):
        return '{classname} (id = "{id}", text = "{text}", odds = {odds}, winner = "{winner}")'.format (
            classname = self.__class__.__name__,
            id   = self.id,
            text = self.text,
            odds = self.odds,
            winner = self.winner,
        )

    @property
    def id (self):
        if self._new:
            raise LookupError ('outcome not saved')

        return self._id

    @id.setter
    def id (self, v):
        self._id = v

    @property
    def db (self):
        return self._db

    @db.setter
    def db (self, v):
        self._db = v

    @property
    def text (self):
        return self._text

    @text.setter
    def text (self, v):
        self._text = v

    @property
    def odds (self):
        return self._odds

    @odds.setter
    def odds (self, v):
        self._odds = D(v)

    @property
    def winner (self):
        return self._winner

    @winner.setter
    def winner (self, v):
        self._winner = v
