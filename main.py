from typing import Optional

from fastapi import FastAPI, Request, Response

app = FastAPI()

users = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/play/{game_id}")
async def game(
    game_id: str,
    request: Request
    ):

    user_id = request.cookies.get("user_id", None)
    if user_id not in users:
        user_id = str(len(users))
        users[user_id] = dict(
            name="New User",
        )

    response = Response(
        content=str({"game_id": game_id, "user_id": user_id, "user": users[user_id]}),
    )
    response.set_cookie(key="user_id", value=user_id)

    return response

@app.get("/update_user")
async def update_user(key:str, value:str, request: Request):
    user_id = request.cookies.get("user_id", None)
    if user_id is None:
        return {"message": "User not found"}

    users[user_id][key] = value

    return {"message": "User updated", "user": users[user_id]}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}