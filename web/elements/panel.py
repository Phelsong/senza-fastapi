"""App layout: persistent chrome (header, panel) + router content area.

Site components are plain functions composing `pyscript.web` classes. The app
router is passed in so links bind to the same router that owns the views.
"""

from pyscript import web
from senza.router import Router


def panel(app_router: Router, *links: tuple[str, str]) -> web.nav:
    """A nav rail of router links: `panel(app_router, ("Hello", "/hello"))`."""
    bar = web.nav(id="panel")
    for text, path in links:
        bar.append(app_router.link(text, path, classes=["panel-link"]))
    return bar


def layout(app_router: Router) -> web.div:
    """Header + panel + the router's content root. Returns the content root
    so the caller can assign it to `app_router.root`."""
    shell = web.div(id="shell")
    shell.append(web.header(web.h1("senza"), classes=["site-header"]))
    body_row = web.div(id="content-row")
    body_row.append(
        panel(
            app_router,
            ("Hello World", "/hello"),
            ("WebSocket Demo", "/test_page"),
        )
    )
    content = web.main(id="main")
    body_row.append(content)
    shell.append(body_row)
    web.page.body.append(shell)
    return content
