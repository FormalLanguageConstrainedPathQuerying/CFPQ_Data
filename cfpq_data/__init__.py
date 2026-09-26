"""
CFPQ_Data
=========

CFPQ_Data is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex Graphs and Grammars used for
experimental analysis of context-free path querying algorithms
"""

import logging

from cfpq_data.config import *
from cfpq_data.dataset import *
from cfpq_data.graphs import *
from cfpq_data.queries import *

__version__ = VERSION

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]>%(levelname)s>%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
