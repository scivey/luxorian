from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, ListField, ReferenceField, StringField, URLField

from server.db.hero import Hero, PlayerHero
from server.db.player import Player
from server.db.talent import Talent


class Replay(Document):
    id = IntField(required=True, primary_key=True)
    date = DateTimeField(required=True)
    heroes_winning = ListField(ReferenceField(Hero))
    heroes_losing = ListField(ReferenceField(Hero))
    length = IntField(required=True)
    map = StringField(required=True, max_length=50)
    mode = StringField(required=True, max_length=25)
    players_losing = ListField(ReferenceField(Player))
    players_winning = ListField(ReferenceField(Player))
    region = IntField(required=True)
    url = URLField(required=True)
    version = StringField(required=True, max_length=25)
    bans = ListField(ReferenceField(Hero))


class PlayerReplay(Document):
    player = ReferenceField(Player, required=True)
    replay = ReferenceField(Replay, required=True)
    hero = ReferenceField(PlayerHero, required=True)
    hero_level = IntField(required=True)
    mmr_before = IntField(required=True)
    mmr_after = IntField()
    talents = ListField(ReferenceField(Talent))
    kills = IntField()
    assists = IntField()
    deaths = IntField()
    time_dead = IntField()
    hero_damage = IntField()
    siege_damage = IntField()
    healing = IntField()
    self_healing = IntField()
    damage_taken = IntField()
    experience_earned = IntField()
