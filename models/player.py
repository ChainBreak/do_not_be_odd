import dataclasses
from models import game
import codename
import uuid


class Player():
    def __init__(self, session_id: str, game: "game.Game"):
        self.session_id = session_id
        self.game = game
        self.id = str(uuid.uuid4())
        self.name = codename.codename(capitalize=True, separator="_")
    
    def playing_this_round(self) -> bool:
        return self in self.game.get_current_round().players
    
    def is_ready(self) -> bool:
        return self in self.game.get_current_round().ready_players