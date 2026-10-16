# libs
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import Config as UV_CONFIG
from uvicorn import Server as UV_SERVER

# imports
from routers.nav import nav
from routers.pyscript_source import pyscript_source

# from fast_socket import websocket_endpoint


# =============================================================================
# print(os.environ.get("SITE_ENV")
server_config: UV_CONFIG = UV_CONFIG(
    app="main:app", host="0.0.0.0", port=8062, root_path="."
)

site_env = os.environ.get("SITE_ENV")
match site_env:
    case "PRODUCTION":
        server_config.log_level = "info"
        server_config.headers.append(("Cache-Control", "must-revalidate"))
        server_config.workers = 8
    case _:
        server_config.reload = True
        server_config.log_level = "trace"
        server_config.ssl_certfile = "./certs/cert.pem"
        server_config.ssl_keyfile = "./certs/key.pem"
        # Starlette/FastApi etag implementation is actually working, this keeps client assets from caching indefinitely
        server_config.headers.append(("Cache-Control", "must-revalidate"))
        # server_config.headers.append(("Pragma", "no-cache"))
        server_config.workers = 16


server: UV_SERVER = UV_SERVER(server_config)


app = FastAPI()
origins: list[str] = [
    "http://localhost",
    "http://127.0.0.1",
    "http://[::]",
    "https://dev.local",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------

app.mount(path="/public", app=StaticFiles(directory="public"), name="public")
# self-hosted pyodide / LSP sources, downloaded by senza/utils scripts
Path("packages").mkdir(exist_ok=True)
app.include_router(nav)
app.include_router(pyscript_source)
app.mount(path="/packages", app=StaticFiles(directory="packages"), name="packages")
# ---------------------------------------------------------
# NOTE: `/senza` and `/web` are intentionally NOT mounted as static files.
# Browser code is served (and thus allow-listed) by routers/pyscript_source.py
app.include_router(nav)
app.include_router(pyscript_source)
# ---------------------------------------------------------


@app.get("/status")
def get_status() -> dict[str, str]:
    return {"status": "ok"}


# ------------------------------------------------------------------------------


@app.websocket("/ws")
async def ws_test(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            await websocket.send_bytes(data)
    except WebSocketDisconnect:
        pass  # client went away; nothing to clean up


if __name__ == "__main__":
    server.run()
