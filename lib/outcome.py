import lib.byh as byh
import db

class Outcome (byh.Byh):

    def __init__ (self, **kwa):
        text = kwa.get ('text')
        odds = kwa.get ('odds')

        super().__init__ ()

        self._new = True
        self._text = text
        self._odds = odds

    def __repr__ (self):
        return '%(classname)s (text = %(text)s, odds = %(odds)s)' % dict (
            classname = self.__class__.__name__,
            text = self.text,
            odds = self.odds,
        )

    #
    # properties
    #

    @property
    def text (self):
        return self._text

    @text.setter
    def text (self, v):
        self._text = v

    @property
    def odds (self):
        return self._odds

    @odds.setter
    def odds (self, v):
        self._odds = int (v)

    @property
    def id (self):
        return self._db.id
