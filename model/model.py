from collections import defaultdict
import dataclasses
import multiprocessing
import random
import threading
import uuid
from loguru import logger
import traceback

class Model():

    def __init__(self):
        traceback.print_stack()
        logger.info("Creating new model")
        self.users = defaultdict(self.create_new_user)
        self.active_games = {}

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
        logger.info(f"Created new game with id {game_id}")
        logger.info(f"{self}")
        logger.info(f"Process name: {multiprocessing.current_process().name}")
        logger.info(f"Thread name: {threading.current_thread().name}")
    
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
