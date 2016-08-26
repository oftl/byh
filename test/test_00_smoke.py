import unittest

import lib.person as person
import lib.bet as bet
import lib.wager as wager
import test.base

class TestSmoke (test.base.TestBase):

    def test_person (self):
        jon = person.Person (
            nick = 'jon',
            pw = 'jon',
            hats = '99',
        )

        self.assertTrue (jon.auth (pw = 'jon'))
        self.assertEqual (jon.nick, 'jon')
        self.assertEqual (jon.hats, 99)

        jon.hats = 101
        self.assertEqual (jon.hats, 101)
