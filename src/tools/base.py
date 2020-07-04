import argparse
from abc import ABC, abstractmethod


class Tool(ABC):

    @abstractmethod
    def init_parser(self, parser: argparse.ArgumentParser):
        parser.parse_args()

    @abstractmethod
    def eval(self, args: argparse.Namespace):
        pass
