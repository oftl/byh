import logging

import lib.payout.simple

class Payout (object):
    """ classes implementing Payout must implement payout
    """

    logger = logging.getLogger('byhlog')

    def __init__ (self, **kwa):
        self.bet = kwa.get ('bet')

        self.strategy = dict (
            simple = lib.payout.simple.Simple ()
        ).get (self.bet.payout_strategy)

        if not self.strategy:
            raise LookupError ('payout strategy <{}> not available'.format (strategy))

    def payout (self):
        payout_factor = self.bet.pot / self.bet.wins
        self.logger.info ('[settle bet <{}>] pot: {}'.format (self.bet.id, self.bet.pot))
        self.logger.info ('[settle bet <{}>] inputs: {}'.format (self.bet.id, self.bet.inputs))
        self.logger.info ('[settle bet <{}>] total wins: {}'.format (self.bet.id, self.bet.wins))
        self.logger.info ('[settle bet <{}>] payout factor: {}'.format (self.bet.id, payout_factor))

        self.logger.info ('Payout.payout() called')
        self.strategy.payout()
