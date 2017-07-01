import unittest

import lib.db
from lib.bet import Bet
from lib.user import User

def main():
        db = lib.db.db

        db.create_tables ([
            lib.db.User,
            lib.db.Bet,
            lib.db.Wager,
            lib.db.Outcome,
        ])

        lib.db.User.create (
            nick = 'neil',
            pwhash = 'd68e939882371200637d5024b360fc20',  # neil
            hats = 101,
        )

        lib.db.User.create (
            nick = 'mike',
            pwhash = '18126e7bd3f84b3f3e4df094def5b7de',  # mike
            hats = 101,
        )

        lib.db.User.create (
            nick = 'buzz',
            pwhash = 'b9056d71aca02a3a7fb860f66864fef0',  # buzz
            hats = 101,
        )

        laika = User (
            nick = 'laika',
            pw = 'laika',
            hats = 101,
        )
        laika.save()
        user_id = laika.id

        derby = Bet (
            owner    = laika,
            text     = 'Who will win the next Derby ?',
            outcomes = [
                dict (text = 'Rapid',   odds = 2.00),
                dict (text = 'Austria', odds = 2.00),
            ]
        )
        derby.save()
        bet_id = derby.id

        derby = Bet (
            owner    = laika,
            text     = 'Who will win the Fruit Cup ?',
            outcomes = [
                dict (text = 'Gramatneusiedel', odds = 1.20),
                dict (text = 'Oed im Winkel',   odds = 1.80),
            ]
        )
        derby.save()
        bet_id = derby.id

if __name__ == '__main__':
    main() 
