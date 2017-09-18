from mongoengine.document import Document
from mongoengine.fields import BooleanField, DateTimeField, IntField, ReferenceField, StringField, DictField

from server.db.player import Player


class Hero(Document):
    name = StringField(required=True)
    description = StringField()
    release_date = DateTimeField()
    blizz_role = StringField()
    bans = DictField()
    can_tank = BooleanField(default=False)
    can_solo_heal = BooleanField(default=False)
    can_heal_ally = BooleanField(default=False)
    can_heal_self = BooleanField(default=False)
    can_shield_self = BooleanField(default=False)
    can_shield_ally = BooleanField(default=False)
    can_solo_lane = BooleanField(default=False)
    has_aoe_heal = BooleanField(default=False)
    has_dot_heal = BooleanField(default=False)
    has_percent_heal = BooleanField(default=False)
    has_aoe_damage = BooleanField(default=False)
    has_dot_damage = BooleanField(default=False)
    has_percent_damage = BooleanField(default=False)
    has_waveclear = BooleanField(default=False)
    has_global = BooleanField(default=False)
    has_stun = BooleanField(default=False)
    has_root = BooleanField(default=False)
    has_slow = BooleanField(default=False)
    has_silence = BooleanField(default=False)
    has_blind = BooleanField(default=False)
    has_sleep = BooleanField(default=False)
    has_polymorph = BooleanField(default=False)
    has_knockback = BooleanField(default=False)
    has_stasis = BooleanField(default=False)
    has_time_stop = BooleanField(default=False)
    has_parry = BooleanField(default=False)
    has_unrevealable = BooleanField(default=False)
    has_reveal = BooleanField(default=False)
    has_stealth_self = BooleanField(default=False)
    has_stealth_ally = BooleanField(default=False)
    has_evade_self = BooleanField(default=False)
    has_evade_ally = BooleanField(default=False)
    has_unstoppable_self = BooleanField(default=False)
    has_unstoppable_ally = BooleanField(default=False)
    has_protected_self = BooleanField(default=False)
    has_protected_ally = BooleanField(default=False)
    has_unkillable_self = BooleanField(default=False)
    has_unkillable_ally = BooleanField(default=False)
    has_invulnerable_self = BooleanField(default=False)
    has_invulnerable_ally = BooleanField(default=False)
    has_aa_speedup_ally = BooleanField(default=False)
    has_aa_speedup_self = BooleanField(default=False)
    has_move_speedup_ally = BooleanField(default=False)
    has_move_speedup_self = BooleanField(default=False)
    has_aa_dpsup_ally = BooleanField(default=False)
    has_aa_dpsup_self = BooleanField(default=False)
    has_crits_ally = BooleanField(default=False)
    has_crits_self = BooleanField(default=False)
    has_ability_dpsup_ally = BooleanField(default=False)
    has_ability_dpsup_self = BooleanField(default=False)

    def __repr__(self):
        return '{}'.format(self.name)

    def get_hero_popularity(self):
        popularity = {'players': 0, 'total_level': 0}
        for player_hero in PlayerHero.objects(hero=self):
            if player_hero.mode not in popularity:
                popularity[player_hero.mode] = {
                    'wins': 0,
                    'losses': 0,
                    'bans': self.bans[player_hero.mode]
                }
            popularity[player_hero.mode]['losses'] += player_hero.games_played - player_hero.games_won
            popularity[player_hero.mode]['wins'] += player_hero.games_won
            popularity['players'] += 1
            popularity['total_level'] += player_hero.level
        return popularity

    def get_hero_popularity_for_date_range(self, start_date, end_date=None, min_level=1, mode=None):
        from server.db.replay import Replay
        popularity = {}
        replays_by_result = Replay.get_replays_by_result_for_hero_mode_and_date_range(self, start_date, end_date, mode,
                                                                                      min_level)
        for result, replays in replays_by_result.items():
            for replay in replays:
                if replay.mode not in popularity:
                    popularity[replay.mode] = {
                        'wins': 0,
                        'losses': 0,
                        'bans': 0
                    }
                popularity[replay.mode][result] += 1
        return popularity

    def get_talents_details(self):
        return {}

    def get_hero_details(self):
        hero_details = {'talents': self.get_talents_details(), 'popularity': self.get_hero_popularity()}
        return hero_details


class PlayerHero(Document):
    player = ReferenceField(Player, required=True)
    hero = ReferenceField(Hero, required=True)
    mode = StringField(required=True)
    level = IntField(required=True, default=1)
    games_played = IntField(required=True, default=0)
    games_won = IntField(required=True, default=0)

    def __repr__(self):
        data_dict = {'level': self.level, 'games_played': self.games_played, 'games_won': self.games_won}
        return '{}: {}'.format(self.hero.name, data_dict)
