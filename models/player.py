import dataclasses
from models import game
import codename
import uuid
@dataclasses.dataclass
class Player():
    session_id: str
    game: "game.Game"
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    name: str = dataclasses.field(default_factory=codename.codename)
    playing: bool = False