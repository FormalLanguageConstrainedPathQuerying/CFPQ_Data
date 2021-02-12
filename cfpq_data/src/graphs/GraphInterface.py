from abc import *


class GraphInterface(ABC):
    @classmethod
    @abstractmethod
    def build(cls, *args):
        pass

    @classmethod
    @abstractmethod
    def load(cls, path_to_graph=None, file_extension='rdf'):
        pass

    @abstractmethod
    def save(self, path_to_graph=None, file_extension='rdf', config=None):
        pass

    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def save_metadata(self):
        pass
