from collections import defaultdict
import dataclasses
import uuid


class Model():

    def __init__(self):
        self.users = defaultdict(self.create_new_user)

    @dataclasses.dataclass

    def create_new_user():
        return User(
            id=str( uuid.uuid4() ),
            name="New User",
        )


class User():
    id: str
    name: str
