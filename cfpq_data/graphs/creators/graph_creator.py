"""Interface for graph creators.
"""

from abc import ABC, abstractmethod

from networkx import DiGraph

__all__ = ["GraphCreator"]


class GraphCreator(ABC):
    """Interface for graph creators."""

    @abstractmethod
    def create(self) -> DiGraph:
        """Graph creation function."""
        pass
