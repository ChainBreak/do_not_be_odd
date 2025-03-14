from pydantic import BaseModel
from models import game, player

class GameSchema(BaseModel):
    game_id: str
    current_state: str
    this_player: "PlayerSchema"
    num_players: int
    player_list: list["PlayerSchema"]
    round_number: int

    def __init__(self,game: game.Game, player: player.Player):
        super().__init__(
            game_id = game.id,
            round_number = game.round_number,
            current_state = game.current_state,
            this_player = PlayerSchema(player),
            num_players = len(game.players),
            player_list = [PlayerSchema(other_player) for other_player in game.players.values()],
        )

class PlayerSchema(BaseModel):
    name: str
    id: str
    playing_this_round: bool
    ready: bool

    def __init__(self,player: player.Player):
        super().__init__(
            name=player.name,
            id=player.id,
            playing_this_round=player.playing_this_round(),
            ready=player.is_ready(),
        )

