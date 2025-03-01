
from loguru import logger
from models import player


class Game():
    def __init__(self, game_id: str):
        self.id:str = game_id
        self.players: dict[str,player.Player] = dict()

    def get_or_add_new_player(self, session_id: str) -> "player.Player":
        if session_id not in self.players:
            new_player = player.Player(session_id=session_id, game=self)
            self.players[session_id] = new_player
            logger.info(f"Added player {new_player} to game {self.id}")

        return self.players[session_id]
    
