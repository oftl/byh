import hashlib

from lib.byh import Byh
from lib.outcome import Outcome
from lib.wager import Wager
import db

class Bet (Byh):

    def __init__ (self, **kwa):
        text     = kwa.get ('text')
        owner    = kwa.get ('owner')
        outcomes = kwa.get ('outcomes')

        super().__init__ ()

        if kwa.get ('id') and len (kwa) == 1:
            self.load (**kwa)

        elif text and owner and outcomes:
            self._new = True

            self._text  = text
            self._owner = owner

            self._outcomes = [
                Outcome (
                    text = o.get ('text'),
                    odds = o.get ('odds'),
                )
                for o in outcomes
            ]

        else:
            raise UserWarning ('missing params')

    def load (self, **kwa):
        id = kwa.get ('id')

        data = db.Bet.get (db.bet.id == id)

        self._id = id
        self._text = data.text
        self._owner = Person (nick = data.owner.nick)
        self._outcomes = [
            Outcome (
                text = o.text,
                odds = o.odds,
            )
            for o in data.outcomes
        ]

        self._db = data

    def save (self):
        if self._new:
            self._db = db.Bet.create (
                text = self._text,
                owner = self._owner._db,
            )

            for o in self._outcomes:
                o.set_db (db.Outcome.create (
                    bet = self._db,
                    text = o.text,
                    odds = o.odds,
                ))

            self._new = False

        else:
            self._db.text = self._text
            self._db.owner = self._owner.id
            self._db.hats = self._hats
            self._db.outcomes = self._outcomes  # ?!

            self._db.save()

    def place (self, **kwa):
        owner = kwa.get ('owner')
        outcome = kwa.get ('outcome')
        hats  = kwa.get ('hats')

        w = Wager (
            owner = owner,
            bet   = self,
            outcome = outcome,
            hats  = hats,
        )

        w.save()

    def __repr__ (self):
        return '%(classname)s (text = "%(text)s", owner = %(owner)s, outcomes = %(outcomes)s)' % dict (
            classname = self.__class__.__name__,
            text = self.text,
            owner = repr(self.owner),
            outcomes = repr(self.outcomes),
        )

    #
    # properties
    #

    @property
    def owner (self):
        return self._owner

    @property
    def text (self):
        return self._text

    @text.setter
    def text (self, v):
        self._text = v

    # outcomes can only be access (r and w) as a whole list
    #
    @property
    def outcomes (self):
        return self._outcomes

    @outcomes.setter
    def outcomes (self, v):
        self._text = v
