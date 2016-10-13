import hashlib

import lib.byh as byh
import db

class Outcome (byh.Byh):

    def __init__ (self, **kwa):
        super().__init__ ()

        if kwa.get ('id') and len (kwa) == 1:
            self.load (**kwa)
        else:
            self.create (**kwa)

    def load (self, **kwa):
        self.data = db.Outcome.get (db.Outcome.id == kwa.get ('id'))

    def create (self, **kwa):
        self.data = db.Outcome.create (
            bet = kwa.get ('bet'),
            text = kwa.get ('text'),
            odds = kwa.get ('odds'),
        )

    ###

    def __repr__ (self):
        return '%(classname)s (bet = "%(bet)s", text = %(text)s, odds = %(odds)s)' % dict (
            classname = self.__class__.__name__,
            bet = repr (self.data.bet),
            text = self.data.text,
            odds = self.data.odds,
        )

    #
    # properties
    #

    @property
    def text (self):
        return self.data.text

    @text.setter
    def text (self, v):
        self.data.text = v
        self.data.save()

    @property
    def odds (self):
        return self.data.odds

    @odds.setter
    def odds (self, v):
        self.data.odds = int (v)
        self.data.save()

    # @property
    # def bet (self):
    #     return self.data.bet

    # @bet.setter
    # def bet (self, v):
    #     self.data.bet = int (v)
    #     self.data.save()
