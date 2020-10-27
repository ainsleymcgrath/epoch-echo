"""Quick & Dirty util for syncing pyproject.toml's version with __version__.
Kind of a bummer that it has to exist :/
Requires that dev dependencies are installed."""

from pathlib import Path

from toml import decoder  # available from `pre-commit` dev dependency

from ee_cli import __version__ as app_version

if __name__ == "__main__":
    toml_version = decoder.load(Path("pyproject.toml"))["tool"]["poetry"]["version"]
    if app_version != toml_version:
        print("Versions out of sync :(")
        print(f"ee_cli version:           {app_version}")
        print(f"pyproject.toml version:   {toml_version}")
        exit(1)

    print("Versions match!")
    exit(0)
