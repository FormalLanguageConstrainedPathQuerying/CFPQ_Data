from cfpq_data_devtools.filters import *

DATA_DIR = 'data'
MATRICES = 'Matrices'
GRAMMARS = 'Grammars'


def get_matrix_dir(suite, data_path=DATA_DIR):
    return os.path.join(data_path, suite, MATRICES)


def get_grammar_dir(suite, data_path=DATA_DIR):
    return os.path.join(data_path, suite, GRAMMARS)


class DataWrapper:
    def __init__(self, data_path=DATA_DIR):
        self.data_path = data_path

    def get_suites(self):
        return os.listdir(self.data_path)

    def get_graphs(self, suite,
                   include_extensions=None, exclude_extensions=None,
                   max_file_size=None, min_file_size=None,
                   max_file_len=None, min_file_len=None,
                   ignore_hidden_files=True):
        matrix_dir = get_matrix_dir(suite, self.data_path)
        graph_filter = all_filter_combinator(
            lambda g: file_has_extension(g, include_extensions),
            lambda g: exclude_extensions is None or not file_has_extension(g, exclude_extensions),
            lambda g: file_has_size(os.path.join(matrix_dir, g), min_file_size, max_file_size),
            lambda g: file_has_len(os.path.join(matrix_dir, g), min_file_len, max_file_len),
            lambda g: not file_is_hidden(g) if ignore_hidden_files else True
        )
        graphs = os.listdir(matrix_dir) if os.path.exists(matrix_dir) else []
        return [os.path.join(matrix_dir, graph) for graph in graphs
                if graph_filter(graph)]

    def get_grammars(self, suite, include_extension=None):
        grammar_dir = get_grammar_dir(suite, self.data_path)
        grammar_filter = all_filter_combinator(
            lambda gr: file_has_extension(gr, include_extension)
        )
        grammars = os.listdir(grammar_dir) if os.path.exists(grammar_dir) else []
        return [os.path.join(grammar_dir, grammar) for grammar in grammars
                if grammar_filter(grammar)]
