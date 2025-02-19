from collections import defaultdict
import dataclasses
import random
import uuid
from loguru import logger

class Model():

    def __init__(self):
        logger.info("Creating new model")
        self.users = defaultdict(self.create_new_user)
        self.active_games = {}
        self.test_dict = dict()

    def get_user(self, user_id):
        return self.users[user_id]
    
    def create_new_user(self):
        return User(
            id=str( uuid.uuid4() ),
            name="New User",
        )

    def create_new_game(self) -> "Game":
        game_id = self.get_unique_game_id()
        
        game = Game(
            id=game_id,
        )

        self.active_games[game_id] = game
        self.test_dict.update( {game_id:"hi"})

        logger.info(f"Created new game with id {game_id}")
        logger.info(f"Games: {self.active_games}")
        logger.info(f"test: {self.test_dict}")
        return game
    
    def get_unique_game_id(self):
        # max retries to avoid infinite loop
        for _ in range(100):
            game_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', k=4))
            if game_id not in self.active_games:
                return game_id
            
        raise ValueError("Could not generate a unique game id")

@dataclasses.dataclass
class Game():
    id: str
    players: list["User"] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class User():
    id: str
    name: str
