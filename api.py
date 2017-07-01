#!/usr/bin/env python3

from bottle import request, response, route, post, get, run, template
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


mk_url = lambda path: '{scheme}://{host}/{path}'.format (
    scheme = request.urlparts[0],
    host   = request.urlparts[1],
    path   = path,
)


@get('/bets')
def bets():
    bets = lib.bet.Bets().bets

    response.set_header('Content-Type', 'application/vnd.collection+json')

    return json.dumps (
        dict (
            collection = dict (
                version = '1.0',
                href = '/bets',
                items = [
                    dict (
                        href  = mk_url ('bet/{bet_id}'.format (bet_id = bet.id)),
                        # a partial representation of a single bet
                        data = [
                            # also prompt is allowed here!
                            dict ( name = 'text', value = bet.text ),
                            dict ( name = 'owner_nick', value = bet.owner.nick ),
                            dict ( name = 'owner_id', value = bet.owner.id ),
                        ],
                        links = [
                            dict (
                                # also prompt and name are allowed here!
                                href = mk_url ('bet/{bet_id}/bet'.format (bet_id = bet.id)),
                                rel = 'do_bet',
                                render = 'link',
                            ),
                            dict (
                                href = mk_url ('user/{owner_id}'.format (owner_id = bet.owner.id)),
                                rel = 'owner',
                                render = 'link',
                            ),
                        ],
                    ) for bet in bets
                ],
                links = [
                    dict (href = mk_url (''), rel = 'home', render = 'link'),
                ],
                queries = [
                    dict (
                        href = mk_url ('search'),
                        rel = 'search',
                        prompt = 'Search for bets',
                        data = [ dict (name = 'query', value = '') ],
                    )
                ],
                template = dict (
                    data = [
                        dict ( prompt = 'Text of new bet', name = 'text', value = ''),
                        # dict ( prompt = 'Owner', name = 'owner', value = logged_in_user),
                    ]
                ),
                # error = dict (title = None, code = None, message = None),
                error = None,
            ),
        ),
        # cls = lib.bet.BetJSONEncoder,  # here be magic
    )

@get ('/bet/<bet_id>')
def read_bet (bet_id):
    bet = lib.bet.Bet (id = bet_id)

    response.set_header('Content-Type', 'application/vnd.collection+json')

    return json.dumps (
        dict (
            collection = dict (
                version = '1.0',
                href = mk_url ('bet/{bet_id}'.format (bet_id = bet_id)),
                items = [
                    dict (
                        href = mk_url ('bet/{bet_id}'.format (bet_id = bet_id)),
                        # a partial representation of a single bet
                        data = [
                            dict (
                                name = 'text',
                                prompt = 'Text of bet',
                                value = bet.text,
                            ),
                            dict (
                                name = 'owner_nick',
                                prompt = 'Nick of owner',
                                value = bet.owner.nick,
                            ),
                            dict (
                                name = 'owner_id',
                                prompt = 'Internal id of owner',
                                value = bet.owner.id,
                            ),
                        ],
                    ),
                ],
                #  links = [
                #      dict (href = mk_url (''), rel = 'home', render = 'link'),
                #  ],
                #  queries = [
                #      dict (
                #          href = mk_url ('search'),
                #          rel = 'search',
                #          prompt = 'Search for bets',
                #          data = [ dict (name = 'query', value = '') ],
                #      )
                #  ],
                #  template = dict (
                #      data = [
                #          dict ( prompt = 'Text of new bet', name = 'text', value = ''),
                #          # dict ( prompt = 'Owner', name = 'owner', value = logged_in_user),
                #      ]
                #  ),
                #  # error = dict (title = None, code = None, message = None),
                #  error = None,
            ),
        ),
        # cls = lib.bet.BetJSONEncoder,  # here be magic
    )

run (
    host = 'localhost',
    port = 8080,
)
