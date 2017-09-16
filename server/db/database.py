import logging

from dateutil import parser
from mongoengine import connect, DoesNotExist
from trueskill import Rating, TrueSkill

from server.db.hero import PlayerHero, Hero
from server.db.player import Player, PlayerModeDetails
from server.db.replay import Replay, PlayerReplay
from server.exceptions import ReplayAlreadyExists, UntrackedReplay

logger = logging.getLogger('server.db.database')


class Database:
    def __init__(self):
        self.db_connection = connect('mongo_luxorian', host='localhost', port=27017)


class LeagueDatabase(Database):
    def __init__(self):
        super(LeagueDatabase, self).__init__()


class ReplayDatabase(Database):
    GAME_MODES = {'QuickMatch', 'UnrankedDraft', 'HeroLeague', 'TeamLeague'}

    def __init__(self):
        self.trueskill_env = TrueSkill(mu=1700.0, sigma=1700.0 / 3.0, beta=1700.0 / 6.0, tau=1700.0 / 300.0,
                                       draw_probability=0.0)
        super(ReplayDatabase, self).__init__()

    @staticmethod
    def get_latest():
        latest_replay = Replay.objects.order_by('-id').limit(-1).first()
        return latest_replay.id if latest_replay else -1

    @staticmethod
    def get_or_add_hero(hero_name):
        try:
            hero = Hero.objects(name=hero_name).get()
        except DoesNotExist:
            hero = Hero(name=hero_name)
            hero.save()
            logger.info('Found Hero {} ({})'.format(hero_name, hero.pk))
        return hero

    def add_or_update_player(self, player_data, replay):
        try:
            player = Player.objects(blizz_id=player_data['blizz_id']).get()
        except DoesNotExist:
            player = Player(
                blizz_id=player_data['blizz_id'],
                battletag=player_data['battletag']
            )
            player.save()
            for mode in self.GAME_MODES:
                details = PlayerModeDetails(player=player, mode=mode)
                details.save()
            logger.info('Found and added Player {} ({})'.format(player.battletag, player.blizz_id))

        self.update_player_details(player, replay, player_data['hero'], player_data['hero_level'])  # TODO: add talents
        return player

    def update_player_details(self, player, replay, hero_name, hero_level):  # TODO: add talents
        player_details = player.get_player_details(replay.mode)
        hero = [hero for hero in player_details.get_heroes() if hero.hero.name == hero_name]
        if len(hero) == 1:
            hero = hero[0]
        else:
            hero_char = self.get_or_add_hero(hero_name)
            hero = PlayerHero(player=player, hero=hero_char, mode=replay.mode)
            logger.info('Added PlayerHero {} ({}) for Player {} ({})'.format(hero_char.name, hero.id, player.battletag,
                                                                             player.blizz_id))

        hero.level = hero_level
        hero.games_played += 1
        hero.games_won += 1
        hero.save()

        player_replay = PlayerReplay(player=player,
                                     replay=replay,
                                     hero=hero,
                                     hero_level=hero_level,
                                     mmr_before=player_details.mmr)
        player_replay.save()
        logger.info(
            'Added PlayerReplay {} for Player {} ({})'.format(player_replay.pk, player.battletag, player.blizz_id))

        logger.info('Updated Player {} ({})'.format(player.battletag, player.blizz_id))

    def update_player_mmr(self, replay):
        winning_ratings = {player: Rating(player.get_player_details(replay.mode).mmr,
                                          player.get_player_details(replay.mode).mmr_certainty) for player in
                           replay.players_winning}
        losing_ratings = {player: Rating(player.get_player_details(replay.mode).mmr,
                                         player.get_player_details(replay.mode).mmr_certainty) for player in
                          replay.players_losing}
        recalculated_ratings = self.trueskill_env.rate([winning_ratings, losing_ratings])
        for (player, rating) in [player_rating for team in recalculated_ratings for player_rating in team.items()]:
            player_details = player.get_player_details(replay.mode)
            player_details.mmr = rating.mu
            player_details.mmr_certainty = rating.sigma
            player_details.save()

            player_replay = player.get_player_replay(replay, replay.mode)
            player_replay.mmr_after = rating.mu
            player_replay.save()

            msg = 'Updated {} MMR [{} -> {}] for Player {} ({})'.format(replay.mode, player_replay.mmr_before,
                                                                        rating.mu, player.battletag, player.blizz_id)
            logger.info(msg)

    def parse_replay(self, replay_data):
        if replay_data['game_type'] not in self.GAME_MODES:
            raise UntrackedReplay

        try:
            Replay.objects(id=replay_data['id']).get()
            logger.error('Tried to parse Replay {} but it already existed'.format(replay_data['id']))
            raise ReplayAlreadyExists
        except DoesNotExist:
            pass

        replay = Replay(
            id=replay_data['id'],
            date=parser.parse(replay_data['game_date']),
            heroes_losing=[self.get_or_add_hero(player['hero']) for player in replay_data['players'] if
                           not player['winner']],
            heroes_winning=[self.get_or_add_hero(player['hero']) for player in replay_data['players'] if
                            player['winner']],
            length=replay_data['game_length'],
            map=replay_data['game_map'],
            mode=replay_data['game_type'],
            region=replay_data['region'],
            url=replay_data['url'],
            version=replay_data['game_version']
        )
        replay.save()  # initial save to store to DB so PlayerReplay can reference it
        replay.players_losing.extend([self.add_or_update_player(player, replay) for player in replay_data['players'] if
                                 not player['winner']]),
        replay.players_winning.extend([self.add_or_update_player(player, replay) for player in replay_data['players'] if
                                  player['winner']]),
        replay.save()
        logger.info('Parsed Replay {}'.format(replay.id))

        self.update_player_mmr(replay)

        return replay_data['id']
