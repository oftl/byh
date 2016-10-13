import db

class Byh (object):

    def __init__ (self):
        # connection would also happen transparently
        # as soon as queries are run
        db.db.connect()
        self.db = db.db

        # True if self.data differs from storage
        self._dirty = False

        self._new = False

    def log (msg):
        print (msg)

    @property
    def id (self):
        if self.data.id:
            return self.data.id
        else:
            raise LookupError ('object has no member "id"')
