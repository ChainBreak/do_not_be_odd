
from loguru import logger
from models import session
from models import player


class Game():
    def __init__(self, game_id: str):
        self.id:str = game_id
        self.players: dict[str,player.Player] = dict()

    def add_new_player(self, session: session.Session) -> "player.Player":
        new_player = player.Player(session=session, game=self)
        self.players[session.id] = new_player
        logger.info(f"Added player {new_player} to game {self.id}")
        return new_player

    


