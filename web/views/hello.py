"""The minimal page: everything a senza view needs in nine lines."""

from pyscript import web


def hello() -> web.div:
    return web.div(
        web.h2("Hello World"),
        web.p(
            "A senza view is a plain function returning pyscript.web elements.",
            classes=["muted"],
        ),
    )
