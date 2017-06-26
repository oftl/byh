import lib.payout.payout as payout

class Simple (payout.Payout):

    def __init__ (self, **kwa):
        self.bet = kwa.get ('bet')

    def payout (self):
        self.logger.info ('Simple.payout() called')
        assert (self.bet.wins != 0)

        # payout_factor
        pf = self.bet.pot / self.bet.wins

        self.logger.info ('[settle bet <{}>] pot: {}'.format (self.bet.id, self.bet.pot))
        self.logger.info ('[settle bet <{}>] wins: {}'.format (self.bet.id, self.bet.wins))
        self.logger.info ('[settle bet <{}>] pf: {}'.format (self.bet.id, pf))

        payed = 0

        if pf >= 1:
            for w in self.bet.wagers_won:
                win = w.hats * self.bet.outcome_won.odds
                w.owner.hats += win
                w.owner.save ()
                payed += win

            assert (payed < self.bet.pot)

            # split surplus evenly among all winners
            #  return_factor = (self.bet.pot - self.bet.wins) / self.bet.pot
            #  for w in self.bet.wagers:
            #      returning = w.hats * return_factor
            #      w.owner.hats += returning
            #      w.owner.save ()
            #      payed += returning

            # ... or surplus goes to the owner of the bet

            self.logger.info (
                '[settle bet <{}>] bet owner gets surplus of {}'.format (
                self.bet.id,
                self.bet.pot - payed,
            ))

            surplus = (self.bet.pot - payed)
            payed += surplus
            self.bet.owner.hats += surplus
            self.bet.owner.save()

        elif pf < 1:
            for w in self.bet.wagers_won:
                win = pf * w.hats * self.bet.outcome_won.odds
                w.owner.hats += win
                w.owner.save ()
                payed += win

        self.logger.info ('[settle bet <{}>] payed: {}'.format (self.bet.id, payed))

        assert (payed == self.bet.pot)
