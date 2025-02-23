import fastapi
from fastapi.staticfiles import StaticFiles

import routes.templates
import routes.websockets
import routes.operations


app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(routes.templates.router)
app.include_router(routes.websockets.router)
app.include_router(routes.operations.router)
