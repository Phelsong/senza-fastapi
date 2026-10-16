"""Push the local senza core workspace copy to the upstream senza repository.

senza-fastapi no longer vendors senza as a git submodule: `senza/` here is a
workspace-only copy (git-ignored), and this script syncs its core into
`../senza` (the Phelsong/senza checkout referenced by other projects'
submodules) so you can review/commit it there once.

Copied: core modules, utils, README, pyproject, releases.txt (the pin history).
Skipped: `*-delete` leftovers, sass, scratch, caches.

Usage:
    python scripts/upstream_senza.py [--target ../senza] [--bootstrap]
    --bootstrap: additionally pull the checked-out senza repo's core files in
    (one-time conversion from a submodule checkout to a workspace copy).
"""

import shutil
import sys
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parents[1]
CORE_FILES = [
    "router.py",
    "config.py",
    "releases.py",
    "compiler.py",
    "visibility.py",
    "README.md",
    "pyproject.toml",
    "releases.txt",
]
CORE_DIRS = ["scripts"]
SKIP_PATTERNS = ("*-delete", "*-delete/", "__pycache__", "*.pyc", ".sass-cache")


def _copy_file(src: Path, dst_dir: Path) -> str:
    dst_dir.mkdir(parents=True, exist_ok=True)
    target = dst_dir / src.name
    target.write_bytes(src.read_bytes())
    return target.as_posix()


def sync(target: Path, workspace: Path = HERE) -> dict[str, str]:
    if not (target / ".git").exists():
        raise SystemExit(f"error: {target} does not look like a git checkout of senza")
    senza_ws = workspace / "senza"
    if not senza_ws.is_dir():
        raise SystemExit(f"error: {workspace}/senza missing — nothing to sync")
    report: dict[str, str] = {}
    for name in CORE_FILES:
        src = senza_ws / name
        if not src.is_file():
            print(f"  skip (missing here): {name}")
            continue
        report[name] = _copy_file(src, target)
    for name in CORE_DIRS:
        src = senza_ws / name
        if src.is_dir():
            for f in src.glob("*.py"):
                report[f"{name}/{f.name}"] = _copy_file(f, target / name)
    return report


def bootstrap(target: Path, workspace: Path = HERE) -> dict[str, str]:
    """One-time: copy the senza repo's core files into the workspace copy."""
    senza_ws = workspace / "senza"
    senza_ws.mkdir(parents=True, exist_ok=True)
    report: dict[str, str] = {}
    for name in [*CORE_FILES, "sass", "utils"]:
        src = target / name
        if src.is_file():
            report[name] = (
                (senza_ws / name).as_posix()
                if not (senza_ws / name).write_bytes(src.read_bytes())
                else (senza_ws / name).as_posix()
            )
        elif src.is_dir() and name in ("utils",):
            (senza_ws / name).mkdir(exist_ok=True)
            for f in src.glob("*.py"):
                _copy_file(f, senza_ws / name)
                report[f"{name}/{f.name}"] = (senza_ws / name / f.name).as_posix()
    return report


def main(argv: Optional[list[str]] = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)

    def flag(flag_name: str, default: str) -> str:
        if flag_name in args:
            i = args.index(flag_name)
            value = args[i + 1]
            del args[i : i + 2]
            return value
        if default:
            return str((HERE / default).resolve())
        return default

    target = Path(flag("--target", "../senza")).resolve()
    if "--bootstrap" in args:
        if (HERE / "senza" / "router.py").is_file():
            print("workspace already bootstrapped; skipping")
        else:
            for name, dest in bootstrap(target).items():
                print(f"bootstrapped {name} -> {dest}")
        return
    report = sync(target)
    print(f"synced {len(report)} files -> {target}")
    for name, dest in sorted(report.items()):
        print(f"  {name} -> {dest}")
    print("(commit and push the senza repo, then update other projects)")


if __name__ == "__main__":
    main()
