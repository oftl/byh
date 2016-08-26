import hashlib

import lib.byh as byh
import db

class Person (byh.Byh):

    def __init__ (self, **kwa):
        # self.db ..... database connection
        # self.data ... loaded peewee object

        super().__init__ ()

        if kwa.get ('nick') and len (kwa) == 1:
            self.load (**kwa)
        else:
            self.create (**kwa)

    def load (self, **kwa):
        self.data = db.Person.get (db.Person.nick == kwa.get ('nick'))

    def create (self, **kwa):
        self.data = db.Person.create (
            nick = kwa.get ('nick'),
            pwhash = hashlib.md5(kwa.get ('pw').encode()).hexdigest(),
            hats = int (kwa.get ('hats')),
        )

    def auth (self, **kwa):
        if not self.data:
            raise UserWarning ('no person loaded')

        return self.data.pwhash == hashlib.md5 (kwa.get ('pw').encode()).hexdigest()

    # properties
    #

    @property
    def nick (self):
        return self.data.nick

    @nick.setter
    def nick (self, v):
        self.data.nick = v
        self.data.save()

    @property
    def hats (self):
        return self.data.hats

    @hats.setter
    def hats (self, v):
        self.data.hats = int (v)
        self.data.save()
