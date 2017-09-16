import logging

from mongoengine.document import Document
from mongoengine.fields import FloatField, IntField, ReferenceField, StringField

logger = logging.getLogger('server.db.player')


class Player(Document):
    blizz_id = IntField(required=True)
    battletag = StringField(required=True, max_length=12)

    def get_player_details(self, game_mode=None):
        if game_mode:
            player_details = [detail for detail in PlayerModeDetails.objects(player=self) if detail.mode == game_mode]
            if len(player_details) == 1:
                return player_details[0]
            else:
                msg = 'Could not find PlayerDetails for Player {} in {}'.format(self.blizz_id, game_mode)
                logger.error(msg)
                raise AttributeError(msg)
        else:
            player_details = PlayerModeDetails.objects(player=self)
            return player_details

    def get_player_replay(self, replay, game_mode=None):
        from server.db.replay import PlayerReplay

        if game_mode:
            found_replay = [r for r in self.get_player_details(game_mode).get_replays() if r.replay == replay]
        else:
            found_replay = [r for r in PlayerReplay.objects(player=self) if r.replay == replay]
        if len(found_replay) == 1:
            return found_replay[0]
        else:
            msg = 'Could not find PlayerReplay for Player {} and Replay {}'.format(self.blizz_id, replay.id)
            logger.error(msg)
            raise AttributeError(msg)


class PlayerModeDetails(Document):

    player = ReferenceField(Player, required=True)
    mode = StringField(required=True)
    mmr = FloatField(required=True, default=1700.0)
    mmr_certainty = FloatField(required=True, default=1700.0 / 3.0)

    def get_replays(self):
        from server.db.replay import PlayerReplay
        player_mode_replays = [r for r in PlayerReplay.objects(player=self.player) if r.replay.mode == self.mode]
        return player_mode_replays

    def get_heroes(self):
        from server.db.hero import PlayerHero
        player_heroes = [h for h in PlayerHero.objects(player=self.player) if h.mode == self.mode]
        return player_heroes

    def get_talents(self):
        from server.db.talent import PlayerTalent
        player_talents = [t for t in PlayerTalent.objects(player=self.player) if t.mode == self.mode]
        return player_talents

