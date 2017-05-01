import unittest
import lib.db as db
from lib.bet import Bet
from lib.user import User

class TestBase (unittest.TestCase):

    def setUp (self):
        self.db = db.db
        # self.db.connect()  # happens transparently when db is accessed

        self.db.create_tables ([
            db.User,
            db.Bet,
            db.Wager,
            db.Outcome,
        ])

    def create_users (self):

        db.User.create (
            nick = 'neil',
            pwhash = 'd68e939882371200637d5024b360fc20',  # neil
            hats = 101,
        )

        db.User.create (
            nick = 'mike',
            pwhash = '18126e7bd3f84b3f3e4df094def5b7de',  # mike
            hats = 101,
        )

        db.User.create (
            nick = 'buzz',
            pwhash = 'b9056d71aca02a3a7fb860f66864fef0',  # buzz
            hats = 101,
        )

    def create_bets (self):
        laika = User (
            nick = 'laika',
            pw = 'laika',
            hats = 101,
        )
        laika.save()
        self.user_id = laika.id

        derby = Bet (
            owner    = laika,
            text     = 'Who will win the next Derby ?',
            outcomes = [
                dict (text = 'Rapid',   odds = 4.60),
                dict (text = 'Austria', odds = 4.60),
            ]
        )
        derby.save()
        self.bet_id = derby.id

    def tearDown (self):
        db.User.drop_table()
        db.Bet.drop_table()
        db.Wager.drop_table()
        db.Outcome.drop_table()

        self.db.close()
