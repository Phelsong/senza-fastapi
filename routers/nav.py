# libs
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from utils.pyscript_release import shell_html

# imports


# =============================================================================

nav = APIRouter(
    prefix="",
    tags=["page shells"],
    responses={404: {"description": "Not found"}},
)

# =============================================================================
# Every page served by the backend renders the same pyscript shell: one pinned
# runtime, one entry script (`web/app.py`). The server-side route makes the URL
# shareable/deep-linkable; the client-side router in `senza/router.py` handles
# in-app navigation without reloads.


@nav.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(shell_html("Pyscript App"), status_code=200)


@nav.get("/hello", response_class=HTMLResponse)
def hello_page() -> HTMLResponse:
    return HTMLResponse(shell_html("Hello World"), status_code=200)


@nav.get("/test_page", response_class=HTMLResponse)
def test_page_view() -> HTMLResponse:
    return HTMLResponse(shell_html("WebSocket Demo"), status_code=200)


@nav.get("/about", response_class=HTMLResponse)
def about() -> HTMLResponse:
    return HTMLResponse(shell_html("About"), status_code=200)
