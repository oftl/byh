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

        self.outcomes = [
            lib.outcome.Outcome (
                _new   = self._new,
                id     = oc.id,
                text   = oc.text,
                odds   = oc.odds,
                # winner = oc.winner,
                db     = oc,
            )
            for oc in self.db.outcomes
        ]


    def create (self, **kwa):
        self._new  = True
        self.owner = kwa.get ('owner')
        self.text  = kwa.get ('text')

        self.outcomes = [
            lib.outcome.Outcome (
                _new   = self._new,
                text   = oc.get ('text'),
                odds   = oc.get ('odds'),
                # winner = oc.get ('winner'),
            )
            for oc in kwa.get ('outcomes')
        ]


    def save (self):
        if self._new:
            self.db = db.Bet.create (
                owner = self.owner.db,
                text  = self.text,
            )

            self.id = self.db.id

            for oc in self.outcomes:
                new_o = db.Outcome.create (
                    _new   = self._new,
                    bet    = self.db,
                    text   = oc.text,
                    odds   = oc.odds,
                    # winner = oc.winner,
                )

                oc.db = new_o
                oc.id = new_o.id

            self._new = False

        else:
            self.db.owner = self.owner
            self.db.text  = self.text
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
        outcome = kwa.get ('outcome')
        outcome.winner = True
        # outcome.save()
        wins = 0
        inputs = 0

        for w in self.wagers:
            inputs += w.hats
            if w.outcome.id == outcome.id:
                wins += w.hats * outcome.odds

        assert (self.pot == inputs)

        payout_factor = self.pot / wins

        logging.info ('[settle bet <{}>] pot: {}'.format (self.id, self.pot))
        logging.info ('[settle bet <{}>] inputs: {}'.format (self.id, inputs))
        logging.info ('[settle bet <{}>] total wins: {}'.format (self.id, wins))
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
    def pot (self):
        res = 0
        for w in self.wagers:
            res += w.hats
        return res
