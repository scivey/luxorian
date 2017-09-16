from mongoengine import Document, IntField, ReferenceField, StringField

from server.db.hero import Hero
from server.db.player import Player


class Talent(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    hero = ReferenceField(Hero, required=True)
    level = IntField()
    games_played = IntField(required=True, default=0)
    games_won = IntField(required=True, default=0)


class PlayerTalent(Document):
    player = ReferenceField(Player, required=True)
    talent = ReferenceField(Talent, required=True)
    mode = StringField(required=True)
    games_played = IntField(required=True, default=0)
    games_won = IntField(required=True, default=0)
