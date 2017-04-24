import hashlib

import lib.byh
import lib.account
import lib.wager
import lib.db as db

class User (lib.byh.Byh, lib.account.Account):

    def __init__ (self, **kwa):
        id   = kwa.get ('id')
        nick = kwa.get ('nick')
        hats = kwa.get ('hats')
        pw   = kwa.get ('pw')

        if (nick or id) and len (kwa) == 1:
            self.load (**kwa)
        elif nick and hats and pw:
            self.create (**kwa)
        else:
            raise UserWarning


    def load (self, **kwa):
        nick = kwa.get ('nick')
        id   = kwa.get ('id')

        if nick:
            u = db.User.get (db.User.nick == nick)
        elif id:
            u = db.User.get (db.User.id == id)
        else:
            raise UserWarning

        self._new    = False
        self.nick   = u.nick
        self.pwhash = u.pwhash
        self.hats   = u.hats
        self.db     = u


    def create (self, **kwa):
        self._new   = True
        self.nick   = kwa.get ('nick')
        self.hats   = kwa.get ('hats')
        self.pwhash = pw2hash (pw = kwa.get ('pw'))


    def save (self):
        if self._new:
            self.db = db.User.create (
                nick   = self.nick,
                pwhash = self.pwhash,
                hats   = int (self.hats),
            )

            self._id = self.db.id

            self._new = False

        else:
            self.db.nick   = self.nick
            self.db.pwhash = self.pwhash
            self.db.hats   = self.hats
            self.db.save()


    def auth (self, **kwa):
        return pw2hash (pw = kwa.get ('pw')) == self.pwhash


    def __repr__ (self):
        return '%(classname)s (nick = "%(nick)s", hats = %(hats)s)' % dict (
            classname = self.__class__.__name__,
            # id   = self.id,
            nick = self.nick,
            hats = self.hats,
        )

    @property
    def db (self):
        return self._db

    @db.setter
    def db (self, v):
        self._db = v

    @property
    def id (self):
        if self._new:
            raise LookupError ('user not saved')

        return self.db.id

    @property
    def nick (self):
        return self._nick

    @nick.setter
    def nick (self, v):
        self._nick = v

    @property
    def hats (self):
        return self.balance

    @hats.setter
    def hats (self, v):
        self.balance = v

    @property
    def pwhash (self):
        return self._pwhash

    @pwhash.setter
    def pwhash (self, v):
        self._pwhash = v

    @property
    def wagers (self):
        return [ lib.wager.Wager (id = w.id) for w in self.db.wagers ]

### helpers
###

def pw2hash (**kwa):
    return hashlib.md5 (kwa.get ('pw').encode()).hexdigest()

