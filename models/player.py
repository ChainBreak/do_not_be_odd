import dataclasses
from models import session, game

@dataclasses.dataclass
class Player():
    session: session.Session
    game: "game.Game"
    name: str = "Player"