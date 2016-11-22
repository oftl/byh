from peewee import *

db = SqliteDatabase ('byh.db')

class Person (Model):
    nick = CharField()
    pwhash = CharField()
    hats = BigIntegerField()
    created = TimestampField()

    class Meta:
        database = db

class Bet (Model):
    owner = ForeignKeyField (Person, related_name = 'bets')
    text  = CharField()

    class Meta:
        database = db

class Outcome (Model):
    bet    = ForeignKeyField (Bet, related_name = 'outcomes')
    text   = CharField()
    odds   = BigIntegerField()
    winner = BooleanField(null=True)

    class Meta:
        database = db

class Wager (Model):
    owner   = ForeignKeyField (Person, related_name = 'wagers')
    bet     = ForeignKeyField (Bet, related_name = 'wagers')
    outcome = ForeignKeyField (Outcome, related_name = 'wagers')
    hats    = BigIntegerField()

    class Meta:
        database = db

# class Ground
