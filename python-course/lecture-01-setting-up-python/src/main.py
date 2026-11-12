"""First script: check that the project environment is set up correctly."""
import sys
from importlib.metadata import version

import requests
from rich.console import Console
from rich.table import Table

PACKAGES = ["requests", "rich"]


def latest_version(package: str) -> str:
    """Ask PyPI for the newest released version of a package."""
    url = f"https://pypi.org/pypi/{package}/json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["info"]["version"]


def in_virtualenv() -> bool:
    return sys.prefix != sys.base_prefix


def main() -> None:
    console = Console()
    console.print(f"Python {sys.version.split()[0]}")
    console.print(f"Running from: {sys.executable}")
    console.print(f"Virtual environment active: {in_virtualenv()}")

    table = Table(title="Installed vs latest on PyPI")
    table.add_column("package")
    table.add_column("installed")
    table.add_column("latest")
    for name in PACKAGES:
        table.add_row(name, version(name), latest_version(name))
    console.print(table)


if __name__ == "__main__":
    main()
