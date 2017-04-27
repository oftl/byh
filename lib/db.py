import os

from peewee import *

DB_FILENAME = './BYH_TEST_DATABASE'
DB = SqliteDatabase (DB_FILENAME)

class User (Model):
    nick = CharField()
    pwhash = CharField()
    hats = BigIntegerField()
    created = TimestampField()

    class Meta:
        database = DB

class Bet (Model):
    owner = ForeignKeyField (User, related_name = 'bets')
    text  = CharField()
    settled = BooleanField (null=True)
    payout_strategy = CharField()

    class Meta:
        database = DB

class Outcome (Model):
    bet    = ForeignKeyField (Bet, related_name = 'outcomes')
    text   = CharField()
    odds   = BigIntegerField()
    winner = BooleanField(null=True)

    class Meta:
        database = DB

# # which outcome(s) won
# class BetOutcome (Model):
#     bet     = ForeignKeyField (Bet, related_name = 'winner')
#     outcome = ForeignKeyField (Outcome)
# 
#     class Meta:
#         database = DB

class Wager (Model):
    owner   = ForeignKeyField (User, related_name = 'wagers')
    bet     = ForeignKeyField (Bet, related_name = 'wagers')
    outcome = ForeignKeyField (Outcome, related_name = 'wagers')
    hats    = BigIntegerField()

    class Meta:
        database = DB

# class Ground

db = DB
