import logging

import lib.payout.simple

class Payout (object):
    """ classes implementing Payout must implement payout
    """

    logger = logging.getLogger('byhlog')

    def __init__ (self, **kwa):
        # self.bet is the context in GOF terms
        bet = kwa.get ('bet')

        # select strategy / payout algorithm to use
        #
        self.strategy = dict (
            simple = lib.payout.simple.Simple (bet = bet)
        ).get (bet.payout_strategy)

        if not self.strategy:
            raise LookupError ('payout strategy <{}> not available'.format (self.bet.payout_strategy))

    def payout (self):
        self.logger.info ('Payout.payout() called')
        self.strategy.payout()
