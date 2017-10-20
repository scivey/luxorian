from mongoengine.document import Document
from mongoengine.fields import DateTimeField, IntField, ListField, ReferenceField, StringField, URLField, BooleanField

from server.db.hero import Hero, PlayerHero
from server.db.player import Player
from server.db.talent import Talent


class Replay(Document):
    id = IntField(required=True, primary_key=True)
    date = DateTimeField(required=True)
    heroes_winning = ListField(ReferenceField(PlayerHero))
    heroes_losing = ListField(ReferenceField(PlayerHero))
    length = IntField(required=True)
    map = StringField(required=True, max_length=50)
    mode = StringField(required=True, max_length=25)
    players_losing = ListField(ReferenceField(Player))
    players_winning = ListField(ReferenceField(Player))
    region = IntField(required=True)
    url = URLField(required=True)
    version = StringField(required=True, max_length=25)
    bans = ListField(ReferenceField(Hero))
    meta = {
        'indexes': [
            '-date',
            ('-date', 'mode')
        ]
    }

    @classmethod
    def get_replays_by_result_for_hero_mode_and_date_range(cls, hero, start_date, end_date=None, mode=None,
                                                           min_level=None):
        response = {'wins': [], 'losses': [], 'bans': []}

        if end_date and mode:
            replays = cls.objects(date__gte=start_date, date__lte=end_date, mode=mode)
        elif end_date:
            replays = cls.objects(date__gte=start_date, date__lte=end_date)
        elif mode:
            replays = cls.objects(date__gte=start_date, mode=mode)
        else:
            replays = cls.objects(date__gte=start_date)

        for replay in replays:
            if hero in replay.bans:
                response['bans'].append(replay)
                continue
            player_heroes_winning = [ph for ph in replay.heroes_winning if ph.hero == hero]
            player_heroes_losing = [ph for ph in replay.heroes_losing if ph.hero == hero]
            if len(player_heroes_winning) > 0 and len(player_heroes_losing) > 0:
                continue  # ignore mirror matches
            if len(player_heroes_winning) > 0:
                if not min_level or (min_level and PlayerReplay.objects(player_hero=player_heroes_winning[0],
                                                                        replay=replay).get().hero_level >= min_level):
                    response['wins'].append(replay)
            if len(player_heroes_losing) > 0:
                if not min_level or (min_level and PlayerReplay.objects(player_hero=player_heroes_losing[0],
                                                                        replay=replay).get().hero_level >= min_level):
                    response['losses'].append(replay)
        return response


class PlayerReplay(Document):
    player = ReferenceField(Player, required=True)
    replay = ReferenceField(Replay, required=True)
    is_winner = BooleanField(required=True)
    player_hero = ReferenceField(PlayerHero, required=True)
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
    meta = {
        'indexes': [
            'player_hero',
            'replay',
            ('player_hero', 'replay')
        ]
    }
