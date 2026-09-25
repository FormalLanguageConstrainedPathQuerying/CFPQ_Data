import pathlib

__all__ = [
    "VERSION",
    "ROOT",
    "DATA",
    "GRAPHS_DIR",
]

VERSION = "5.0.0"

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
GRAPHS_DIR = DATA / "graphs"
