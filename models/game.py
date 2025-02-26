import dataclasses
from loguru import logger
from models import session


class Game():
    def __init__(self, game_id: str):
        self.id:str = game_id
        self.players: dict[str,Player] = dict()

    def add_new_player(self, session: session.Session) -> "Player":
        player = Player(session=session, game=self)
        self.players[session.id] = player
        logger.info(f"Added player {player} to game {self.id}")
        return player

    
@dataclasses.dataclass
class Player():
    session: session.Session
    game: Game
    name: str = "Player"

