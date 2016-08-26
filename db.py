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
    name = CharField()

    class Meta:
        database = db

class Wager (Model):
    owner = ForeignKeyField (Person, related_name = 'wagers')
    hats = BigIntegerField()

    class Meta:
        database = db

# class Ground
