from abc import *


class GraphInterface(ABC):
    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def save_metadata(self):
        pass

    @classmethod
    @abstractmethod
    def build(cls, *args):
        pass

    @classmethod
    @abstractmethod
    def from_rdf(cls, path):
        pass

    @abstractmethod
    def to_rdf(self, path):
        pass

    @classmethod
    @abstractmethod
    def from_txt(cls, path):
        pass

    @abstractmethod
    def to_txt(self, path):
        pass
