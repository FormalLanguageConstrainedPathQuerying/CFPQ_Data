"""Interface for graph serializers.
"""

from abc import ABC, abstractmethod

__all__ = ["GraphSerializer"]


class GraphSerializer(ABC):
    """Interface for graph serializers."""

    @abstractmethod
    def serialize(self):
        """Graph serialization function."""
        pass
