
import time
from loguru import logger
from models import player

class Game():
    def __init__(self, game_id: str, time_function: callable = time.time):
        self.id:str = game_id
        self.time_function = time_function
        self.players: dict[str,player.Player] = dict()
        self.rounds = [GameRound()]
    
        self.game_states = {
            "join_round": self.state_join_round,
            "round_start": self.state_round_start,
            "player_turn": self.state_player_turn,
            "show_result": self.state_show_result,
            "round_end": self.state_round_end,
        }
        self.last_state = None
        self.current_state = "join_round"
        self.next_state = self.current_state

    def add_or_get_player(self, session_id: str) -> "player.Player":

        if session_id not in self.players:
            new_player = player.Player(session_id=session_id, game=self)
            self.players[session_id] = new_player
            logger.info(f"Added player {new_player} to game {self.id}")

        return self.players[session_id]
    
    def update(self):
        current_state_callable = self.game_states[self.current_state]
        current_state_callable()
        if self.is_state_first_call():
            logger.info(f"Game {self.id} changed state from {self.last_state} to {self.current_state}")
        self.last_state = self.current_state
        self.current_state = self.next_state

    def is_state_first_call(self):
        return self.last_state != self.current_state
    
    def is_state_last_call(self):
        return self.next_state != self.current_state
    
    def change_state(self, new_state):
        if new_state not in self.game_states:
            raise ValueError(f"State does not exists: {new_state}. Should be one of {self.game_states.keys()}")
        self.next_state = new_state

    def state_join_round(self):
        if self.is_state_first_call():
            self.start_time = self.time_function()
        
        if self.time_function() - self.start_time > 3:
            self.change_state("round_start")

    def state_round_start(self):
        if self.is_state_first_call():
            self.start_time = self.time_function()
        
        if self.time_function() - self.start_time > 3:
            self.change_state("player_turn")

    def state_player_turn(self):
        if self.is_state_first_call():
            self.start_time = self.time_function()
        
        if self.time_function() - self.start_time > 3:
            self.change_state("show_result")
    def state_show_result(self):
        if self.is_state_first_call():
            self.start_time = self.time_function()
        
        if self.time_function() - self.start_time > 3:
            self.change_state("round_end")

    def state_round_end(self):
        if self.is_state_first_call():
            self.start_time = self.time_function()
        
        if self.time_function() - self.start_time > 3:
            self.change_state("round_start")

class GameRound():
    def __init__(self):
        self.num_tasks_in_round = 10
        self.current_task = 0
        self.players = set()