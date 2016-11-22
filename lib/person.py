import hashlib

import lib.byh as byh
import db

class Person (byh.Byh):

    def __init__ (self, **kwa):
        nick = kwa.get ('nick')
        pw   = kwa.get ('pw')
        hats = kwa.get ('hats')

        super().__init__ ()

        if nick and len (kwa) == 1:
            self.load (**kwa)

        elif nick and pw and hats:
            self._new = True

            self._nick = nick
            self._pwhash = hashlib.md5(pw.encode()).hexdigest()
            self._hats = int (hats)

        else:
            raise UserWarning ('missing params')

    def load (self, **kwa):
        nick = kwa.get ('nick')
        data = db.Person.get (db.Person.nick == nick)

        self._nick   = nick
        self._pwhash = data.pwhash
        self._hats   = data.hats
        self._db     = data

    def save (self):
        if self._new:
            self._db = db.Person.create (
                nick   = self._nick,
                pwhash = self._pwhash,
                hats   = int (self._hats),
            )

            self._new = False

        else:
            self._db.nick = self._nick
            self._db.pwhash = self._pwhash
            self._db.hats = self._hats
            self._db.save()

    def auth (self, **kwa):
        pw = kwa.get ('pw')

        return self._pwhash == hashlib.md5 (pw.encode()).hexdigest()

    ###

    def __repr__ (self):
        return '%(classname)s (nick = "%(nick)s", hats = %(hats)s)' % dict (
            classname = self.__class__.__name__,
            nick = self._nick,
            hats = self._hats,
        )

    # properties
    #

    @property
    def nick (self):
        return self._nick

    @nick.setter
    def nick (self, v):
        self._nick = v

    @property
    def hats (self):
        return self._hats

    @hats.setter
    def hats (self, v):
        self._hats = v

    @property
    def pw (self, v):
        self._pwhash = hashlib.md5(self.v.encode()).hexdigest(),
