# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) Josh S Wilkinson
#
# This file is part of the senza project, licensed under the GNU Affero
# General Public License v3.0 (or, at your option, any later version).
# See the LICENSE file at the repository root for the full text.
"""Serves the Python source the browser needs, at `/pyscript-source/<rel-path>`.

Instead of mounting the whole repo as static files (which leaks every server
module), this router whitelists exactly what the browser is allowed to fetch:

- every file listed in `web/config.toml` under `[[fetch]]`
- `web/config.toml` itself (see `CLIENT_ENV_KEYS` below)

Anything else 404s, so server-side code (queries, auth, secrets, routers) is
never served. Paths can't escape the allowlist because lookup is by exact
relative-path key, never by filesystem traversal.

`served_config()` injects a `[env]` table into the config.toml body: only the
environment variables named in `CLIENT_ENV_KEYS` (non-secret ones) reach the
browser. Client code reads them via `from pyscript import config`:
`config["env"]["site_env"]`.
"""

import os
import tomllib
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from utils import project_root

ROOT = Path(project_root)
CONFIG_PATH = ROOT / "web" / "config.toml"

# Environment variables that are safe and useful to expose to the browser.
# Anything not listed here (secrets, keys, internal hosts) is never read.
CLIENT_ENV_KEYS: tuple[str, ...] = ("SITE_ENV",)

# relative path -> absolute path, computed once at startup
_ALLOWED: dict[str, Path] = {"web/config.toml": CONFIG_PATH}

with open(CONFIG_PATH, "rb") as _config_file:
    _config = tomllib.load(_config_file)
# modern config: `[files]` sources like "{FROM}/web/app.py" (or literals)
if "files" in _config:
    _FROM = "{FROM}"
    for _src in _config["files"]:
        if _src == _FROM:
            continue
        if _src.startswith(_FROM + "/"):
            _rel = _src[len(_FROM) + 1 :]
        elif "{" in _src:
            continue  # unknown placeholder, not ours to serve
        else:
            _rel = _src.lstrip("/")
        if _rel.endswith(".py") and _rel not in _ALLOWED:
            _ALLOWED[_rel] = ROOT / _rel
# legacy config: `[[fetch]] files` lists
else:
    for _fetch in _config.get("fetch", []):
        for _rel in _fetch.get("files", []):
            rel = Path(_rel).as_posix()
            if rel.endswith(".py") and rel not in _ALLOWED:
                _ALLOWED[rel] = ROOT / rel

pyscript_source = APIRouter(prefix="/pyscript-source", tags=["pyscript source"])


def allowed_files() -> tuple[str, ...]:
    return tuple(sorted(_ALLOWED))


def served_config() -> str:
    """The config.toml body plus a whitelisted `[env]` table."""
    env_lines = "\n".join(
        f'{key.lower()} = "{os.environ.get(key, "")}"' for key in CLIENT_ENV_KEYS
    )
    body = CONFIG_PATH.read_text().rstrip()
    if env_lines:
        return f"{body}\n\n[env]\n{env_lines}\n"
    return body


_DIST_ROOT = ROOT / "dist" / "pyscript"
_IN_PRODUCTION = os.environ.get("SITE_ENV", "").upper() == "PRODUCTION"


@pyscript_source.get("/{file_path:path}", response_class=PlainTextResponse)
def get_source(file_path: str) -> PlainTextResponse:
    if file_path == "web/config.toml":
        return PlainTextResponse(served_config(), media_type="application/toml")
    target: Optional[Path] = _ALLOWED.get(file_path)
    if target is None or not target.is_file():
        raise HTTPException(status_code=404, detail=f"not served: {file_path}")
    # PRODUCTION serves the minified dist tree built by scripts/compile_dist.py,
    # falling back to source for anything not (yet) compiled
    dist_target = _DIST_ROOT / file_path
    if _IN_PRODUCTION and dist_target.is_file():
        return PlainTextResponse(dist_target.read_text(), media_type="text/x-python")
    return PlainTextResponse(target.read_text(), media_type="text/x-python")
