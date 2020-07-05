import os

from src.utils.filters import *

DATA_DIR = 'data'
MATRICES = 'Matrices'
GRAMMAR = 'Grammar'


def get_matrix_dir(suite, data_path=DATA_DIR):
    return os.path.join(data_path, suite, MATRICES)


def get_grammar_dir(suite, data_path=DATA_DIR):
    return os.path.join(data_path, suite, GRAMMAR)


class DataWrapper:
    def __init__(self, data_path=DATA_DIR):
        self.data_path = data_path

    def get_suites(self):
        return os.listdir(self.data_path)

    def get_graphs(self, suite, include_extensions=None, exclude_extensions=None,
                   max_file_size=None, min_file_size=None):
        matrix_dir = get_matrix_dir(suite, self.data_path)
        graph_filter = all_filter_combinator(
            lambda g: file_has_extension(g, include_extensions),
            lambda g: not file_has_extension(g, exclude_extensions),
            lambda g: file_has_size(os.path.join(matrix_dir, g), min_file_size, max_file_size)
        )
        return [os.path.join(matrix_dir, graph) for graph in os.listdir(matrix_dir)
                if graph_filter(graph)]
