from pydantic import BaseModel
from models import game, player

class GameSchema(BaseModel):
    game_id: str
    player_name: str
    num_players: int
    player_list: list["PlayerSchema"]

    def __init__(self,game: game.Game, player: player.Player):
        super().__init__(
            game_id = game.id,
            player_name = player.name,
            num_players = len(game.players),
            player_list = [PlayerSchema(player) for player in game.players.values()],
        )

class PlayerSchema(BaseModel):
    name: str
    id: str

    def __init__(self,player: player.Player):
        super().__init__(
            name=player.name,
            id=player.id,
        )

