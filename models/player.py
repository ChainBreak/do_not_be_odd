import dataclasses
from models import game

@dataclasses.dataclass
class Player():
    session_id: str
    game: "game.Game"
    name: str = "Player"
    playing: bool = False