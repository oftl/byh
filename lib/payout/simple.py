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

        if pf > 1:
            for w in self.bet.wagers_won:
                win = w.hats * self.bet.outcome_won.odds
                w.owner.add (win)
                w.owner.save ()
                payed += win

            return_factor = (self.bet.pot - self.bet.wins) / self.bet.pot
            for w in self.bet.wagers:
                returning = w.hats * return_factor
                w.owner.add (returning)
                w.owner.save ()
                payed += returning


        elif pf < 1:
            for w in self.bet.wagers_won:
                win = pf * w.hats * self.bet.outcome_won.odds
                w.owner.add (win)
                w.owner.save ()
                payed += win
        else:
            pass

        self.logger.info ('[settle bet <{}>] payed: {}'.format (self.bet.id, payed))
        assert (payed == self.bet.pot)
