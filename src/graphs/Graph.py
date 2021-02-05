from abc import *


class Graph(ABC):
    @abstractmethod
    def get_metadata(self):
        pass

    @abstractmethod
    def save_metadata(self):
        pass
