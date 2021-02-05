import argparse
from abc import *


class CmdParser(ABC):
    @staticmethod
    @abstractmethod
    def init_cmd_parser(parser: argparse.ArgumentParser):
        parser.parse_args()

    @staticmethod
    @abstractmethod
    def eval_cmd_parser(args: argparse.Namespace):
        pass
