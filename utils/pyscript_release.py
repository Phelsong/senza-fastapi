"""FastAPI-side wrapper over the framework-agnostic senza release library.

The library (`senza.releases`) knows how to pin/read pyScript releases and
works for any server. Everything FastAPI-specific lives here: this app's page
shell HTML, rooted at this repo (`utils.project_root`).
"""

from senza import releases
from utils import project_root

# re-export the library surface this app uses, bound to this project's root
__all__ = ["pinned", "core_css", "core_js", "shell_tags", "check"]


def pinned() -> str:
    return releases.pinned(project_root)


def core_css() -> str:
    return releases.core_css(pinned())


def core_js() -> str:
    return releases.core_js(pinned())


def shell_tags() -> str:
    return releases.shell_tags(pinned())


def check() -> str:
    return releases.check(project_root)


SCRIPT_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
"""

SCRIPT_TAIL = """    <title>{title}</title>
</head>
<body>
    <script type="py" src="/pyscript-source/web/app.py" config="/pyscript-source/web/config.toml"></script>
</body>
</html>
"""


def shell_html(title: str) -> str:
    return (
        SCRIPT_HEAD
        + f'    <link rel="stylesheet" href="{core_css()}" />\n'
        + f'    <link defer rel="stylesheet" href="/public/index.css" />\n'
        + f'    <script async defer type="module" src="{core_js()}"></script>\n'
        + SCRIPT_TAIL.format(title=title)
    )
