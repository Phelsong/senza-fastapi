from senza.components.div import Div
from senza.context import site


def sidebar() -> Div:
    sidebar_container = Div(site.body, id="sidebar")

    return sidebar_container
