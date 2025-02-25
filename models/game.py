import dataclasses

from models.user import User

@dataclasses.dataclass
class Game():
    id: str
    players: list["User"] = dataclasses.field(default_factory=list)