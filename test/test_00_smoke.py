import unittest

from lib.person import Person
from lib.bet import Bet
from lib.outcome import Outcome
from lib.wager import Wager

import test.base

class TestSmoke (test.base.TestBase):

    def test_person (self):
        jon = Person (
            nick = 'jon',
            pw = 'jon',
            hats = '99',
        )

        self.assertTrue (jon.auth (pw = 'jon'))
        self.assertEqual (jon.nick, 'jon')
        self.assertEqual (jon.hats, 99)

        jon.hats = 101
        jon.save()

        jon2 = Person (nick = 'jon')

        self.assertEqual (jon.hats, 101)

    def test_bet (self):
        neil = Person (nick = 'neil')

        b1 = Bet (
            text = 'Derby 1970',
            owner = neil.id,
            outcomes = [
                dict (text = 'Rapid', odds = 80),
                dict (text = 'Austria', odds = 20),
            ]
        )

        self.assertEqual (b1.text, 'Derby 1970')
        self.assertEqual (b1.owner.nick, 'neil')
        self.assertEqual (len (b1.outcomes), 2)
