import lib.byh
import lib.db as db
import lib.user
import lib.bet
import lib.outcome

class Wager (lib.byh.Byh):

    def __init__ (self, **kwa):
        id      = kwa.get ('id')
        hats    = kwa.get ('hats')
        owner   = kwa.get ('owner')
        bet     = kwa.get ('bet')
        outcome = kwa.get ('outcome')

        if id and len (kwa) == 1:
            self.load (**kwa)
        elif owner and bet and outcome and hats:
            self.create (**kwa)
        else:
            raise UserWarning


    def load (self, **kwa):
        id = kwa.get ('id')

        self.db = db.Wager.get (db.Wager.id == id)

        self._new    = False
        self.id      = self.db.id
        self.hats    = self.db.hats
        self.owner   = lib.user.User (id = self.db.owner.id)
        self.bet     = lib.bet.Bet (id = self.db.bet.id)
        self.outcome = lib.outcome.Outcome (id = self.db.outcome.id)


    def create (self, **kwa):
        self._new    = True
        self.hats    = kwa.get ('hats')
        self.owner   = kwa.get ('owner')
        self.bet     = kwa.get ('bet')
        self.outcome = kwa.get ('outcome')

    def save (self):
        if self._new:
            self.db = db.Wager.create (
                hats    = self.hats,
                owner   = self.owner.db,
                bet     = self.bet.db,
                outcome = self.outcome.db,
            )

            self.id = self.db.id
            self._new = False


    def __repr__ (self):
        return '{classname} (hats = "{hats}", owner = {owner}, bet = {bet}, outcome = {outcome})'.format (
            classname = self.__class__.__name__,
            # id    = self.id,
            hats    = self.hats,
            owner   = self.owner.nick,
            bet     = self.bet.text,
            outcome = self.outcome.text,
        )


    @property
    def id (self):
        if self._new:
            raise LookupError ('bet not saved')

        return self._id

    @id.setter
    def id (self, v):
        self._id = v

    @property
    def hats (self):
        return self._hats

    @hats.setter
    def hats (self, v):
        self._hats = v

    @property
    def owner (self):
        return self._owner

    @owner.setter
    def owner (self, v):
        self._owner = v

    @property
    def bet (self):
        return self._bet

    @bet.setter
    def bet (self, v):
        self._bet = v

    @property
    def outcome (self):
        return self._outcome

    @outcome.setter
    def outcome (self, v):
        self._outcome = v
