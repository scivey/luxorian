from collections import namedtuple


class Configuration:
    ROOT_URL = 'http://hotsapi.net/api/v1'
    ReplaysParams = namedtuple('ReplayParams', ['start_date', 'end_date', 'game_map', 'game_type', 'player', 'min_id'])
    ReplayParams = namedtuple('ReplayParams', ['battletag', 'hero', 'hero_level', 'team', 'winner', 'region', 'blizz_id'])

    def __init__(self):
        pass

    @property
    def replays_url(self):
        return self.ROOT_URL + '/replays'

    def get_replay_url(self, replay_id):
        return self.replays_url + '/{}'.format(replay_id)
