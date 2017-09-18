import flask

from server.db.player import Player

api = flask.Blueprint('player', __name__)


@api.route('player/<player_id>', methods=['GET'])
def get_player_data(player_id):
    player = Player.objects(blizz_id=player_id).get()
    player_details = player.get_player_details()
    player_ratings = {details.mode: int(round(details.mmr)) for details in player_details}
    player_heroes = {details.mode: [repr(hero) for hero in details.get_heroes()] for details in player_details}

    response = {repr(player): {'ratings': player_ratings, 'heroes': player_heroes}}
    return flask.jsonify(response), 200
