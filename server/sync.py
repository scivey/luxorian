import logging
from http.client import HTTPException
from time import sleep

import requests

from server.config import Configuration
from server.db.database import ReplayDatabase
from server.exceptions import UntrackedReplay, ReplayAlreadyExists, RateLimitExceeded

logger = logging.getLogger('server.sync')


class Sync:
    def __init__(self):
        self.config = Configuration()
        self.db = ReplayDatabase()

    def get_replay_by_id(self, replay_id, battletag=None, hero=None, hero_level=None, team=None, winner=None,
                         region=None, blizz_id=None):
        params = self.config.ReplayParams(battletag=battletag, hero=hero, hero_level=hero_level, team=team,
                                          winner=winner, region=region, blizz_id=blizz_id)

        response = requests.get(self.config.get_replay_url(replay_id),
                                params={k: v for k, v in params._asdict().items() if v})

        if response.status_code == 429:
            logger.info('')
            raise RateLimitExceeded
        elif response.status_code >= 300:
            msg = 'Received HTTP error {} when trying to retrieve Replay {}'.format(response.status_code, replay_id)
            logger.error(msg)
            raise HTTPException(msg)

        return response.json()

    def sync_replay_page(self, latest=None, start_date=None, end_date=None, game_map=None, game_type=None, player=None,
                         min_id=None):
        new_latest = latest or self.db.get_latest()
        params = self.config.ReplaysParams(start_date=start_date, end_date=end_date, game_map=game_map,
                                           game_type=game_type, player=player, min_id=min_id or new_latest + 1)
        response = requests.get(self.config.replays_url, params={k: v for k, v in params._asdict().items() if v})

        if response.status_code == 429:
            logger.info('')
            raise RateLimitExceeded
        elif response.status_code >= 300:
            msg = 'HTTP error {} when trying to retrieve replay page from {}'.format(response.status_code, new_latest)
            logger.error(msg)
            raise HTTPException(msg)

        for replay in response.json():
            try:
                new_latest = self.db.parse_replay(self.get_replay_by_id(replay['id']))
            except UntrackedReplay:
                continue
            except ReplayAlreadyExists:
                continue
            except RateLimitExceeded:
                break

        return new_latest

    def sync_replays(self):
        latest = self.db.get_latest()
        while True:
            try:
                new_latest = self.sync_replay_page(latest)
            except RateLimitExceeded:
                sleep(10)
            if latest == new_latest:
                break
            latest = new_latest


def run_sync():
    sync_server = Sync()
    sync_server.sync_replays()
