import unittest

from lib.person import Person
from lib.bet import Bet
from lib.outcome import Outcome
from lib.wager import Wager

import test.base

class TestSmoke (test.base.TestBase):

    def test_create_person (self):
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

    def test_create_bet (self):
        neil = Person (nick = 'neil')

        b1 = Bet (
            text = 'Derby 1970',
            owner = neil,
            outcomes = [
                dict (text = 'Rapid', odds = 80),
                dict (text = 'Austria', odds = 20),
            ]
        )

        self.assertEqual (b1.text, 'Derby 1970')
        self.assertEqual (b1.owner.nick, 'neil')
        self.assertEqual (len (b1.outcomes), 2)

    def test_create_wager (self):
        neil = Person (nick = 'neil')
        mike = Person (nick = 'mike')

        b1 = Bet (
            text = 'Derby 1970',
            owner = neil,
            outcomes = [
                dict (text = 'Rapid', odds = 80),
                dict (text = 'Austria', odds = 20),
            ]
        )
        b1.save ()

        w1 = Wager (
            bet   = b1,
            owner = mike,
            outcome = list (filter (lambda b: b.text == 'Rapid', b1.outcomes)).pop(),
            hats  = 12,
        )

        # wgr.save()
        # same error as via Bet.place()

        b1.place (
            owner = mike,
            outcome = list (filter (lambda b: b.text == 'Rapid', b1.outcomes)).pop(),
            hats  = 12,
        )

        ##
        self.assertEqual (w1.owner.nick, 'mike')
