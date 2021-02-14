from abc import *
from pathlib import Path
from typing import Optional, Union, Dict


class GraphInterface(ABC):
    """
    Generic graph interface

    """

    @classmethod
    @abstractmethod
    def build(cls, *args):
        """
        Builds graph by arguments

        :param args: various arguments
        :type args: Any
        :return: builded graph
        :rtype: GraphInterface
        """

        pass

    @classmethod
    @abstractmethod
    def load(cls, source: Optional[Union[Path, str]] = None, source_file_format: str = 'rdf'):
        """
        Loads graph from specified destination with specified destination_file_format

        :param source: graph destination
        :type source: Optional[Union[Path, str]]
        :param source_file_format: graph destination_file_format ('txt'/'rdf')
        :type source_file_format: str
        :return: loaded graph
        :rtype: GraphInterface
        """

        pass

    @abstractmethod
    def save(self
             , destination: Optional[Union[Path, str]] = None
             , destination_file_format: str = 'rdf'
             , config: Dict[str, str] = None) -> Path:
        """
        Saves graph with specified destination_file_format and edge configuration

        :param destination: path to save the graph
        :type destination: Optional[Union[Path, str]]
        :param destination_file_format: graph source_file_format
        :type destination_file_format: str
        :param config: edges configuration
        :type config: Dict[str, str]
        :return: path to saved graph
        :rtype:
        """

        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, str]:
        """
        Generates graph metadata

        :return: metadata
        :rtype: Dict[str, str]
        """

        pass

    @abstractmethod
    def save_metadata(self) -> Path:
        """
        Saves metadata to specified file

        :return: path to file with graph metadata
        :rtype: Path
        """

        pass
