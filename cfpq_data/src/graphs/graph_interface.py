from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Dict, Any


class IGraph(ABC):
    """
    Generic graph interface

    """

    @classmethod
    @abstractmethod
    def build(cls, *args: Any) -> IGraph:
        """
        Builds graph by arguments

        :param args: various arguments
        :type args: Any
        :return: built graph
        :rtype: IGraph
        """

    @abstractmethod
    def save(self,
             destination: Union[Path, str],
             destination_file_format: str = 'rdf',
             config: Dict[str, str] = None) -> Path:
        """
        Saves graph with specified destination_file_format and edge configuration

        :param destination: path to save the graph
        :type destination: Optional[Union[Path, str]]
        :param destination_file_format: graph source_file_format
        :type destination_file_format: str
        :param config: edges configuration
        :type config: Dict[str, str]
        :return: path to saved graph
        :rtype: Path
        """

    @abstractmethod
    def get_metadata(self) -> Dict[str, str]:
        """
        Generates graph metadata

        :return: metadata
        :rtype: Dict[str, str]
        """

    @abstractmethod
    def save_metadata(self) -> Path:
        """
        Saves metadata to specified file

        :return: path to file with graph metadata
        :rtype: Path
        """
