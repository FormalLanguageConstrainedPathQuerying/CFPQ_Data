"""
CFPQ_Data
=========

CFPQ_Data is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex Graphs and Grammars used for
experimental analysis of context-free path querying algorithms
"""

import cfpq_data.config
from cfpq_data.config import *

__version__ = VERSION

import cfpq_data.dataset
from cfpq_data.dataset import *

import cfpq_data.graphs
from cfpq_data.graphs import *

import cfpq_data.grammars
from cfpq_data.grammars import *

import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]>%(levelname)s>%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
