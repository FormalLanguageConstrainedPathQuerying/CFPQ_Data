"""
Graphs and grammars for experimental analysis of context-free path querying algorithms

- RDF: Class for loading fixed versions of real-world RDF files
- MemoryAliases: Class for loading real-world data for points-to analysis of C code
- WorstCase: Class for generating graphs with two cycles
- SparseGraph: Class for generating graphs with NetworkX to emulate sparse data
- ScaleFree: Class for generating graphs by using the Barab'asi-Albert model of scale-free networks
- FullGraph: Class for generating cycle graphs, all edges of which are labeled with the same token
- LUBM: Class for generating Lehigh University Benchmark graphs
"""

from cfpq_data.src.graphs.full_graph import FullGraph
from cfpq_data.src.graphs.lubm_graph import LUBM
from cfpq_data.src.graphs.memory_aliases_graph import MemoryAliases
from cfpq_data.src.graphs.rdf_graph import RDF
from cfpq_data.src.graphs.scale_free_graph import ScaleFree
from cfpq_data.src.graphs.sparse_graph import SparseGraph
from cfpq_data.src.graphs.worst_case_graph import WorstCase
