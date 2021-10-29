import pathlib

__all__ = [
    "VERSION",
    "ROOT",
    "DATA",
]

VERSION = "2.0.0"

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
