#!/usr/bin/env python3

import logging
from sanic import Sanic
from sanic import response
from sanic.config import LOGGING

import lib.bet

app = Sanic()

### sanic ###

@app.get ("/")
async def test (request):
    return response.json ({"hello": "world"})


@app.get ("/bets")
async def bets (request):
    bets = lib.bet.Bets().bets
    log.info ('bets: {}'.format (bets))

    return response.json (bets)


### main ###

def get_logger():
    # TODO move to logfile
    handler = logging.FileHandler ('./api.log')
    handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    lgr = logging.getLogger ('api')
    lgr.addHandler (handler)
    lgr.setLevel (logging.INFO)

    return lgr

log = get_logger()
if __name__ == "__main__":
    log.info ('api GO!')
    app.run (host = "0.0.0.0", port = 8000)
