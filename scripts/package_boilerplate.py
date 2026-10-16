"""Package the boilerplate starter project into a tarball.

Walks the repo (including the senza submodule checkout, as plain files) and
archives everything except what the STRIP rules call "repo specific":
private certs, git/venv caches, build outputs, locks, and this project's
runtime state. The result is a drop-in starter tree for a new project.

Usage:
    python scripts/package_boilerplate.py [--out dist/]
    python scripts/package_boilerplate.py --strip certs,docker
"""

import fnmatch
import shutil
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import project_root  # noqa: E402

ROOT = Path(project_root)

# paths never shipped in the boilerplate (glob patterns, relative to root)
STRIP = [
    ".git",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".idea",
    ".pixi",
    ".venv",
    "__pycache__",
    "*.pyc",
    "certs/*",  # private TLS certs
    "build/*",  # old vendored pyscript submodule
    "dist/*",  # build outputs (incl. previous tarballs)
    "public/pyscript/*",  # vendored legacy pyscript runtime (CDN is used now)
    "packages/*",  # downloaded pyodide/LSP artifacts (rebuilt via sync scripts)
    "*-delete",
    "*-delete/*",  # moved-aside legacy files
    "poetry.lock",
    "pixi.lock",  # project-specific lockfiles
]

ADD_SCAFFOLD = {
    "pyscript.version": "2026.7.3\n",  # replaced by this repo's pin at build time
}


def is_stripped(rel: Path) -> bool:
    parts = rel.as_posix()
    for pattern in STRIP:
        if fnmatch.fnmatch(parts, pattern) or fnmatch.fnmatch(rel.name, pattern):
            return True
    return False


def collect() -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if is_stripped(rel) or any(is_stripped(Path(p)) for p in rel.parents):
            continue
        files[rel.as_posix()] = path.read_bytes()
    for name, content in ADD_SCAFFOLD.items():
        files.setdefault(name, content.encode())
    return files


def package() -> Path:
    # start from the live repo's pins, not the scaffold defaults
    ADD_SCAFFOLD["pyscript.version"] = (ROOT / "pyscript.version").read_text()
    files = collect()
    out_dir = ROOT / "dist"
    out_dir.mkdir(exist_ok=True)
    tar_path = out_dir / "senza-fastapi-boilerplate.tar.gz"
    tree = out_dir / "senza-fastapi-boilerplate"
    if tree.exists():
        shutil.rmtree(tree)
    for rel, data in files.items():
        target = tree / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(tree, arcname=tree.name)
    shutil.rmtree(tree)
    print(f"packaged {len(files)} files -> {tar_path}")
    print("remember to update .gitmodules/submodule URLs when installing elsewhere")
    return tar_path


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--strip" in argv:
        i = argv.index("--strip")
        STRIP.extend(argv[i + 1].split(","))
    package()
