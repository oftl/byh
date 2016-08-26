import db

class Byh (object):

    def __init__ (self):
        # connection would also happen transparently
        # as soon as queries are run
        db.db.connect()
        self.db = db.db

    def log (msg):
        print (msg)
