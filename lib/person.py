import hashlib

import lib.byh as byh
import db

class Person (byh.Byh):


    def __init__ (self, **kwa):
        super().__init__ ()

        if ( kwa.get ('nick') or kwa.get ('id') ) and len (kwa) == 1:
            self.load (**kwa)
        else:
            self.create (**kwa)


    def load (self, **kwa):
        if kwa.get ('nick'):
            self.data = db.Person.get (db.Person.nick == kwa.get ('nick'))
        if kwa.get ('id'):
            self.data = db.Person.get (db.Person.id == kwa.get ('id'))


    def create (self, **kwa):
        self.data = db.Person.create (
            nick   = kwa.get('nick'),
            pwhash = hashlib.md5 (kwa.get ('pw').encode()).hexdigest(),
            hats   = int (kwa.get('hats')),
        )

        self._dirty = True


    def save (self):
        if self._dirty:
            self.data.save()
            self._dirty = False


    def auth (self, **kwa):
        pw = kwa.get ('pw')

        return self.data.pwhash == hashlib.md5 (pw.encode()).hexdigest()

    ###

    def __repr__ (self):
        return '%(classname)s (nick = "%(nick)s", hats = %(hats)s)' % dict (
            classname = self.__class__.__name__,
            nick = self.data.nick,
            hats = self.data.hats,
        )

    # properties
    #

    @property
    def nick (self):
        return self.data.nick

    @nick.setter
    def nick (self, v):
        self.data.nick = v

    @property
    def hats (self):
        return self.data.hats

    @hats.setter
    def hats (self, v):
        self.data.hats = v

    @property
    def pw (self, v):
        self.data.pwhash = hashlib.md5(self.v.encode()).hexdigest(),
