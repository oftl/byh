import warnings
import logging

import lib.byh
import lib.db as db
import lib.wager
import lib.outcome

class Bet (lib.byh.Byh):

    def __init__ (self, **kwa):
        owner    = kwa.get ('owner')
        text     = kwa.get ('text')
        outcomes = kwa.get ('outcomes')

        self._wagers_win = None
        self._wins       = None
        self._inputs     = None
        self._winner     = None

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
            self.db = db.Bet.create (
                owner = self.owner.db,
                text  = self.text,
                settled = self.settled,
            )

            self.id = self.db.id

            for oc in self.outcomes:
                new_o = db.Outcome.create (
                    _new   = self._new,
                    bet    = self.db,
                    text   = oc.text,
                    odds   = oc.odds,
                    winner = oc.winner,
                )

                oc.db = new_o
                oc.id = new_o.id

            self._new = False

        else:
            self.db.owner = self.owner
            self.db.text  = self.text
            self.db.settled = self.settled

            warnings.warn ('outcomes can not be updated')

            self.db.save()

    def bet (self, **kwa):
        user    = kwa.get ('user')
        hats    = kwa.get ('hats')
        outcome = kwa.get ('outcome')

        user.sub (hats)

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

        payout_factor = self.pot / self.wins

        logging.info ('[settle bet <{}>] pot: {}'.format (self.id, self.pot))
        logging.info ('[settle bet <{}>] inputs: {}'.format (self.id, self.inputs))
        logging.info ('[settle bet <{}>] total wins: {}'.format (self.id, self.wins))
        logging.info ('[settle bet <{}>] payout factor: {}'.format (self.id, payout_factor))


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
    def pot (self):
        res = 0
        # TODO sum()
        for w in self.wagers:
            res += w.hats
        return res

    @property
    def wagers_win (self, **kwa):
        """returns [ lib.wager.Wager ]
        """

        if not self.settled:
            raise UserWarning ('bet not settled')

        if not self._wagers_win:
            self._wagers_win = filter (
                lambda w: w.outcome.id == self.winner.id,
                self.wagers
            )

        return self._wagers_win

    @property
    def winner (self):
        """returns lib.outcome.Outcome
        """

        if not self.settled:
            raise UserWarning ('bet not settled')

        if not self._winner:
            self._winner = list (filter (
                lambda o: o.winner == True,
                self.outcomes
            )).pop()

            if not self._winner:
                raise UserWarning ('no winning outcome set')

        return self._winner

    @property
    def wins (self):
        if not self.settled:
            raise UserWarning ('bet not settled')

        return sum ([w.hats * self.winner.odds for w in self.wagers_win])

    @property
    def inputs (self):
        if not self.settled:
            raise UserWarning ('bet not settled')

        return sum ([w.hats for w in self.wagers])
