import pathlib

__all__ = [
    "VERSION",
    "ROOT",
    "DATA",
]

VERSION = "4.0.0"

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
