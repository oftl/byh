import unittest
import pprint

import lib.bet
import lib.user
import tests.base

# from peewee import DoesNotExist

class TestSmoke (tests.base.TestBase):

    def setUp (self):
        super().setUp()
        self.create_bets()
        self.create_users()

    def test_001 (self):
        laika = lib.user.User (
            nick = 'laika',
            pw   = 'laika',
            hats = 101,
        )
        laika.save()

        ocs = [
            dict (text = 'Rapid',   odds = 0.8),
            dict (text = 'Austria', odds = 0.2),
        ]

        bet = lib.bet.Bet (
            owner    = laika,
            text     = 'Who will win the next Derby ?',
            outcomes = ocs,
        )

        self.assertEqual ('laika', bet.owner.nick)
        self.assertEqual (len (ocs), len (bet.outcomes))

        with self.assertRaises (LookupError):
            id = bet.id

        bet.save()
        id = bet.id

        bet = lib.bet.Bet (id = id)
        self.assertEqual (len (ocs), len (bet.outcomes))

    def test_002 (self):
        derby  = lib.bet.Bet (id = self.bet_id)
        o0 = derby.outcomes[0]
        o1 = derby.outcomes[1]

        neil = lib.user.User (nick = 'neil')
        buzz = lib.user.User (nick = 'buzz')
        mike = lib.user.User (nick = 'mike')

        derby.bet (
            user    = neil,
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = buzz,
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = mike,
            hats    = 2,
            outcome = o1,
        )

        self.assertEqual (3, len (derby.wagers))
        self.assertEqual (1, len (neil.wagers))

        self.assertEqual (99, neil.hats)
        self.assertEqual (99, buzz.hats)
        self.assertEqual (99, mike.hats)

        derby.settle (outcome = o1)
        self.assertEqual (1, sum (1 for _ in (i for i in derby.wagers_won)))

        # reload for wins/losses
        neil = lib.user.User (nick = 'neil')
        buzz = lib.user.User (nick = 'buzz')
        mike = lib.user.User (nick = 'mike')

        self.assertEqual (99.0, neil.hats)
        self.assertEqual (99.0, buzz.hats)
        self.assertEqual (105.0, mike.hats)
