import warnings
import logging

import lib.byh
import lib.db as db
import lib.wager
import lib.outcome

import lib.payout.simple

class Bet (lib.byh.Byh):

    def __init__ (self, **kwa):
        owner    = kwa.get ('owner')
        text     = kwa.get ('text')
        outcomes = kwa.get ('outcomes')

        self._wagers_won = None
        self._wins       = None
        self._inputs     = None
        self._outcome_won = None

        self.payout_strategy = None

        if id and len (kwa) == 1:
            self.load (**kwa)
        elif owner and text and outcomes:
            self.create (**kwa)
        else:
            raise UserWarning


    def load (self, **kwa):
        id = kwa.get ('id')

        self.db = db.Bet.get (db.Bet.id == id)

        self._new  = False
        self.id    = self.db.id
        self.owner = self.db.owner
        self.text  = self.db.text
        self.settled = self.db.settled
        self.payout_strategy = self.db.payout_strategy

        self.outcomes = [
            lib.outcome.Outcome (
                _new   = self._new,
                id     = oc.id,
                text   = oc.text,
                odds   = oc.odds,
                winner = oc.winner,
                db     = oc,
            )
            for oc in self.db.outcomes
        ]


    def create (self, **kwa):
        self._new  = True
        self.owner = kwa.get ('owner')
        self.text  = kwa.get ('text')
        self.settled = kwa.get ('settled')
        self.payout_strategy = kwa.get ('payout_strategy') or 'simple'

        self.outcomes = [
            lib.outcome.Outcome (
                _new   = self._new,
                text   = oc.get ('text'),
                odds   = oc.get ('odds'),
                winner = oc.get ('winner'),
            )
            for oc in kwa.get ('outcomes')
        ]


    def save (self):
        if self._new:
            self._new = False

            self.db = db.Bet.create (
                owner = self.owner.db,
                text  = self.text,
                settled = self.settled,
                payout_strategy = self.payout_strategy,
            )

            self.id = self.db.id

            for oc in self.outcomes:
                new_o = db.Outcome.create (
                    bet    = self.db,
                    text   = oc.text,
                    odds   = oc.odds,
                    winner = oc.winner,
                )

                oc.db = new_o
                oc.id = new_o.id

        else:
            self.db.owner = self.owner
            self.db.text  = self.text
            self.db.settled = self.settled
            self.db.payout_strategy = self.payout_strategy

            warnings.warn ('outcomes can not be updated')

            self.db.save()

    def bet (self, **kwa):
        user    = kwa.get ('user')
        hats    = kwa.get ('hats')
        outcome = kwa.get ('outcome')

        user.hats -= hats
        user.save ()

        lib.wager.Wager (
            hats    = hats,
            owner   = user,
            bet     = self,
            outcome = outcome,
        ).save()


    def settle (self, **kwa):
        outcome        = kwa.get ('outcome')
        outcome.winner = True
        self.settled   = True

        # strategy as in GOF, Strategy, but selected by Compositor (lib.payout.payout.Payout)
        # parameter bet would be the context (here: self for caller)
        strategy = lib.payout.payout.Payout (bet = self)
        strategy.payout()

    def __repr__ (self):
        ret = '{classname} (owner = "{owner}", text = {text})'.format (
            classname = self.__class__.__name__,
            # id   = self.id,
            owner = self.owner.nick,
            text = self.text,
        )

        for oc in self.outcomes:
            ret += str(oc)

        return ret


    @property
    def id (self):
        if self._new:
            raise LookupError ('bet not saved')

        return self._id

    @id.setter
    def id (self, v):
        self._id = v

    @property
    def owner (self):
        return self._owner

    @owner.setter
    def owner (self, v):
        self._owner = v

    @property
    def text (self):
        return self._text

    @text.setter
    def text (self, v):
        self._text = v

    @property
    def outcomes (self):
        return self._outcomes

    @outcomes.setter
    def outcomes (self, v):
        self._outcomes = v

    @property
    def wagers (self):
        return [ lib.wager.Wager (id = w.id) for w in self.db.wagers ]

    @property
    def settled (self):
        return self._settled

    @settled.setter
    def settled (self, v):
        self._settled = v

    @property
    def payout_strategy (self):
        return self._payout_strategy

    @payout_strategy.setter
    def payout_strategy (self, v):
        self._payout_strategy = v

    @property
    def wagers_won (self, **kwa):
        """returns [ lib.wager.Wager ]
        """

        if not self.settled:
            raise UserWarning ('bet not settled')

        if not self._wagers_won:
            self._wagers_won = list (filter (
                lambda w: w.outcome.id == self.outcome_won.id,
                self.wagers
            ))

        return self._wagers_won

    @property
    def outcome_won (self):
        """returns lib.outcome.Outcome
        """

        if not self.settled:
            raise UserWarning ('bet not settled')

        if not self._outcome_won:
            self._outcome_won = list (filter (
                lambda o: o.winner == True,
                self.outcomes
            )).pop()

            if not self._outcome_won:
                raise UserWarning ('no winning outcome set')

        return self._outcome_won

    @property
    def wins (self):
        if not self.settled:
            raise UserWarning ('bet not settled')

        return sum ([w.hats * self.outcome_won.odds for w in self.wagers_won])

    @property
    def pot (self):
        if not self.settled:
            raise UserWarning ('bet not settled')

        return sum ([w.hats for w in self.wagers])
