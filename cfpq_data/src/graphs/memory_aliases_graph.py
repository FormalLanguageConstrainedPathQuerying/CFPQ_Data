from pathlib import Path
from typing import Dict, Tuple

from cfpq_data.config import RELEASE_INFO
from cfpq_data.src.graphs.rdf_graph import RDF


class MemoryAliases(RDF):
    """
    MemoryAliases — real-world data for points-to analysis of C code

    - graphs: already built graphs
    - graph_keys: reserved graph names
    - config: default edge configuration
    """

    graphs: Dict[Tuple[str, str], Path] = dict()
    graph_keys: Dict[str, str] = RELEASE_INFO['MemoryAliases']
