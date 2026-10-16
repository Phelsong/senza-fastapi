"""App entry point (browser side).

Registers routes, paints the layout, then renders whatever the current URL
points at — so server-served deep links (`/`, `/hello`, `/test_page`) work AND
in-app navigation is instant via the DOM router.
"""

from pyscript import web, window
from senza.router import Router
from web.elements.panel import layout
from web.views.hello import hello
from web.views.test_page import test_page

# one router instance for the whole app — layout links bind to it
app_router = Router()
content = layout(app_router)
app_router.root = content

app_router.add(hello, "/")  # home shows the hello world page
app_router.add(hello, "/hello")
app_router.add(test_page, "/test_page")

# render the view for the URL the server handed us (no history push: the
# browser bar already shows it). Top-level await is pyscript's native entry
# pattern — any failure here is a boot failure, so let it surface.
await app_router.navigate(window.location.pathname, push=False)
