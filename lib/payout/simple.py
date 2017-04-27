import lib.payout.payout as payout

class Simple (payout.Payout):

    def __init__ (self, **kwa):
        # must inherit self.logger
        pass

    def payout (self):
        self.logger.info ('Simple.payout() called')
