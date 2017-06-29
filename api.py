#!/usr/bin/env python3

from bottle import route, post, get, run, template
import logging
import json

import lib.bet

def get_logger():
    # TODO move to logfile
    handler = logging.FileHandler ('./api.log')
    handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    lgr = logging.getLogger ('api')
    lgr.addHandler (handler)
    lgr.setLevel (logging.INFO)

    return lgr

logger = get_logger()

@get('/bets')
def bets():
    bets = lib.bet.Bets().bets

    links = [
       dict (rel = 'index', href = '/'),
    ]

    return json.dumps (dict (
        data = dict (bets = json.dumps (bets, cls=lib.bet.BetJSONEncoder)),
        links = json.dumps (links),
    ))

@post ('/bet/')
def add_bet():
    logger.info (request.json)

#     owner_id = request.forms.get ('owner_id')
#     text = request.forms.get ('text')
#     outcomes = request.forms.get ('text')
#
#         derby = Bet (
#             owner    = laika,
#             text     = 'Who will win the next Derby ?',
#             outcomes = [
#                 dict (text = 'Rapid',   odds = 2.00),
#                 dict (text = 'Austria', odds = 2.00),
#             ]
#         )

run (
    host = 'localhost',
    port = 8080,
)
