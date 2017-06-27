import unittest

import tests.base
from api import app

class TestSmoke (tests.base.TestBase):

    def setUp (self):
        super().setUp()
        self.create_bets()
        self.create_users()

    def test_index_returns_200 (self):
        request, response = app.test_client.get ('/')
        assert response.status == 200

    def test_bets_returns_data (self):
        request, response = app.test_client.get ('/bets')
        assert response.status == 200
