import unittest
import pprint

from lib.user import User
import tests.base

from peewee import DoesNotExist

class TestSmoke (tests.base.TestBase):

    def setUp (self):
        super().setUp()
        self.create_users()

    def test_001 (self):
        jon = User (
            nick   = 'jon',
            pw     = 'jon',
            hats   = 101,
        )

        self.assertEqual('jon', jon.nick)
        self.assertEqual(101, jon.hats)

        # not saved yet
        with self.assertRaises (DoesNotExist):
            User (nick = 'jon')
        with self.assertRaises (LookupError):
            id = jon.id

        jon.save()
        id = jon.id

        jonX = User (id = id)
        self.assertEqual('jon', jonX.nick)

        jonY = User (nick = 'jon')
        self.assertEqual('jon', jonY.nick)

    def test_002 (self):
        buzz = User (nick = 'buzz')
        self.assertEqual ('buzz', buzz.nick)

    def test_003 (self):
        neil = User (nick = 'neil')
        self.assertTrue (neil.auth (pw = 'neil'))
        self.assertFalse (neil.auth (pw = 'wrong pw'))
