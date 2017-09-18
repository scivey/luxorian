import flask
from datetime import datetime, timedelta

from server.db.hero import Hero

api = flask.Blueprint('hero', __name__)


@api.route('hero', methods=['GET'])
def get_sitewide_hero_data():
    now = datetime.utcnow()
    today = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    start_date = today - timedelta(days=7)
    end_date = today - timedelta(microseconds=1)

    hero_stats = {}
    for hero in Hero.objects():
        hero_stats[hero.name] = hero.get_hero_popularity_for_date_range(start_date=start_date, end_date=end_date)

    return flask.jsonify(hero_stats), 200


@api.route('hero/<hero_name>', methods=['GET'])
def get_hero_details(hero_name):
    hero = Hero.objects(name=hero_name).get()
    hero_details = hero.get_hero_details()

    response = {repr(hero): hero_details}
    return flask.jsonify(response), 200
