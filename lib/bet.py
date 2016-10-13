import hashlib

import lib.byh as byh
from lib.outcome import Outcome
import db

class Bet (byh.Byh):

    def __init__ (self, **kwa):

        super().__init__ ()

        if kwa.get ('id') and len (kwa) == 1:
            self.load (**kwa)
        else:
            self.create (**kwa)


    def create (self, **kwa):
        self.data = db.Bet.create (
            owner = kwa.get ('owner'),
            text  = kwa.get ('text'),
        )

        self.data.outcomes = [
            db.Outcome.create (
                bet_id = self.data.id,
                text = o.get('text'),
                odds = o.get('odds'),
            )
            for o in kwa.get ('outcomes')
        ]

        # ok? # self.data.outcomse = ...

#        map (
#            lambda o: db.Outcome.create (
#                bet = self.data.id,
#                text = o.text,
#                odds = o.odds,
#            ),
#            self.kwa.get ('outcomes'),
#        )

        self._new = True


    def load (self, **kwa):
        data = db.Bet.get (db.bet.id == kwa.get ('id'))


    def save (self):
        if self._dirty:
            self.data.save()


    def __repr__ (self):
        return '%(classname)s (text = "%(text)s", owner = %(owner)s, outcomes = %(outcomes)s)' % dict (
            classname = self.__class__.__name__,
            text = self.data.text,
            owner = repr(self.data.owner),
            outcomes = repr(self.data.outcomes),
        )

    #
    # properties
    #

    @property
    def owner (self):
        return self.data.owner

    @property
    def text (self):
        return self.data.text

    @text.setter
    def text (self, v):
        self.data.text = v
        self.data.save()

    # outcomes can only be access (r and w) as a whole list
    #
    @property
    def outcomes (self):
        return [ Outcome (id = o.id) for o in self.data.outcomes ]

    # @outcomes.setter
    # def outcomes (self, v):
        # self.data.outcomes = v
        # self.data.save()
