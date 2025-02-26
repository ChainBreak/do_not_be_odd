import dataclasses

from models.session import Session

@dataclasses.dataclass
class Game():
    id: str
    players: list["Session"] = dataclasses.field(default_factory=list)