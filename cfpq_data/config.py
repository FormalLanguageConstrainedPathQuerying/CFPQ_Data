import pathlib

__all__ = [
    "VERSION",
    "ROOT",
    "DATA",
    "GRAPHS_DIR",
    "GRAMMARS_DIR",
    "BENCHMARKS_DIR",
]

VERSION = "4.0.3"

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"
GRAPHS_DIR = DATA / "graphs"
GRAMMARS_DIR = DATA / "grammars"
BENCHMARKS_DIR = DATA / "benchmarks"
