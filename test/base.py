import unittest
import db

class TestBase (unittest.TestCase):

    def setUp (self):
        self.db = db.db
        self.db.connect()  # happens transparently when db is accessed

        self.db.create_tables ([
            db.Person,
            db.Bet,
            db.Wager,
            db.Outcome,
        ])

        db.Person.create (
            nick = 'neil',
            pwhash = 'e8b7be1d78eb722ce740d28fc62364d9',  # neil
            hats = 101,
        )

        db.Person.create (
            nick = 'mike',
            pwhash = '2ff8557a16f674e466ee4ae619f22758',  # mike
            hats = 101,
        )

        db.Person.create (
            nick = 'buzz',
            pwhash = 'b8b4a79df11085fe608c17f6d7340002',  # buzz
            hats = 101,
        )

    def tearDown (self):
        db.Person.drop_table()
        db.Bet.drop_table()
        db.Wager.drop_table()
        db.Outcome.drop_table()

        self.db.close()
