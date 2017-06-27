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

        derby.bet (
            user    = lib.user.User (nick = 'neil'),
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = lib.user.User (nick = 'buzz'),
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = lib.user.User (nick = 'mike'),
            hats    = 2,
            outcome = o1,
        )

        self.assertEqual (3, len (derby.wagers))
        self.assertEqual (1, len (lib.user.User (nick = 'mike').wagers))

        self.assertEqual (99, lib.user.User (nick = 'neil').hats)
        self.assertEqual (99, lib.user.User (nick = 'buzz').hats)
        self.assertEqual (99, lib.user.User (nick = 'mike').hats)

        derby.settle (outcome = o1)
        self.assertEqual (1, sum (1 for _ in (i for i in derby.wagers_won)))

        self.assertEqual (99, lib.user.User (nick = 'neil').hats)
        self.assertEqual (99, lib.user.User (nick = 'buzz').hats)
        self.assertEqual (103, lib.user.User (nick = 'mike').hats)

    def test_003 (self):
        derby  = lib.bet.Bet (id = self.bet_id)
        o0 = derby.outcomes[0]
        o1 = derby.outcomes[1]

        derby.bet (
            user    = lib.user.User (nick = 'neil'),
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = lib.user.User (nick = 'buzz'),
            hats    = 2,
            outcome = o0,
        )
        derby.bet (
            user    = lib.user.User (nick = 'mike'),
            hats    = 2,
            outcome = o1,
        )

        self.assertEqual (3, len (derby.wagers))
        self.assertEqual (1, len (lib.user.User (nick = 'neil').wagers))

        self.assertEqual (99, lib.user.User (nick = 'neil').hats)
        self.assertEqual (99, lib.user.User (nick = 'buzz').hats)
        self.assertEqual (99, lib.user.User (nick = 'mike').hats)

        derby.settle (outcome = o0)
        self.assertEqual (2, sum (1 for _ in (i for i in derby.wagers_won)))

        self.assertEqual (102, lib.user.User (nick = 'neil').hats)
        self.assertEqual (102, lib.user.User (nick = 'buzz').hats)
        self.assertEqual (99, lib.user.User (nick = 'mike').hats)
