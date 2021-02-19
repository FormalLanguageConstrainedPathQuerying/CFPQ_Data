from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class ICmdParser(ABC):
    """
    Generic command line parser interface

    """

    @staticmethod
    @abstractmethod
    def init_cmd_parser(parser: ArgumentParser):
        """
        Initialize command line parser

        :param parser: WorstCase subparser of command line parser
        :type parser: ArgumentParser
        :return: None
        :rtype: None
        """

        parser.parse_args()

    @staticmethod
    @abstractmethod
    def eval_cmd_parser(args: Namespace):
        """
        Evaluate command line parser

        :param args: command line arguments
        :type args: Namespace
        :return: None
        :rtype: None
        """
