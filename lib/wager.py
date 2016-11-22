import lib.byh as byh
import db

class Wager (byh.Byh):

    def __init__ (self, **kwa):
        owner = kwa.get ('owner')
        bet   = kwa.get ('bet')
        outcome    = kwa.get ('outcome')
        hats  = kwa.get ('hats')

        super().__init__ ()

        if kwa.get ('id') and len (kwa) == 1:
            self.load (**kwa)

        elif owner and bet and outcome:
            self._new = True

            self._owner = owner
            self._bet   = bet
            self._outcome    = outcome
            self._hats  = hats

        else:
            raise UserWarning ('missing params')

    def save (self):
        if self._new:

            self._db = db.Wager.create (
                owner = self._owner._db,
                bet   = self._bet._db,
                outcome = self._outcome._db,
                hats  = self._hats,
            )

            self._new = False

        else:
            self._db.owner = self._owner.id
            self._db.bet   = self._bet.id
            self._db.outcome = self._outcome.id
            self._db.hats  = self._hats

            self._db.save()

    def __repr__ (self):
        return '%(classname)s (bet = "%(bet_id)s", hats = %(hats)s)' % dict (
            classname = self.__class__.__name__,
            bet_id = 'DNTKNW', #self.bet.id,
            hats = self.hats,
        )

    #
    # properties
    #

    @property
    def owner (self):
        return self._owner

    @property
    def bet (self):
        return self._bet

    @property
    def outcome (self):
        return self._outcome

    @property
    def hats (self):
        return self._hats

#    @hats.setter
#    def hats (self, v):
#        self._hats = v
