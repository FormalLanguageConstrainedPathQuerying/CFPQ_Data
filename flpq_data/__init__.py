"""
flpq_data
=========

flpq_data is a Python package for the creation, manipulation, and study of
the structure, dynamics, and functions of complex Graphs and formal-language
queries (regular, context-free, and multiple context-free) used for
experimental analysis of formal-language-constrained path querying algorithms
"""

import logging

from flpq_data.config import *
from flpq_data.dataset import *
from flpq_data.graphs import *
from flpq_data.queries import *

__version__ = VERSION

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]>%(levelname)s>%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
