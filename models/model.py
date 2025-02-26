from collections import defaultdict
import dataclasses
import random
import uuid
from loguru import logger
from models.game import Game
from models.user import User

class Model():

    def __init__(self):

        logger.info("Creating new model")
        self.users = {}
        self.games = {}
    
    def add_new_user(self):

        user = User(
            id=str( uuid.uuid4() ),
            name="New User",
        )

        self.users[user.id] = user

        logger.info(f"Created new user with id {user.id}")
        return user

    def create_new_game(self) -> "Game":
        
        game_id = self.get_unique_game_id()
        
        game = Game(
            id=game_id,
        )

        self.games[game_id] = game
        logger.info(f"Created new game with id {game_id}")
    
        return game
    
    def get_unique_game_id(self):
        # max retries to avoid infinite loop
        for _ in range(100):
            game_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', k=4))
            if game_id not in self.games:
                return game_id
            
        raise ValueError("Could not generate a unique game id")




