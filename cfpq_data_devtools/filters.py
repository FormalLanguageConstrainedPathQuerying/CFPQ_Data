import os
from functools import reduce


def get_file_len(file):
    with open(file, 'r') as f:
        return len(f.readlines())


def any_filter_combinator(*filters):
    return reduce(lambda acc, f: lambda x: acc(x) or f(x), filters, lambda _: False)


def all_filter_combinator(*filters):
    return reduce(lambda acc, f: lambda x: acc(x) and f(x), filters, lambda _: True)


def file_has_extension(file, extensions=None):
    return extensions is None or any([file.endswith(ext) for ext in extensions])


def file_has_size(file, min_size=None, max_size=None):
    size = os.path.getsize(file) // 10 ** 6
    grater_min = min_size is None or min_size < size
    less_max = max_size is None or size < max_size
    return grater_min and less_max


def file_has_len(file, min_length=None, max_length=None):
    length = get_file_len(file)
    grater_min = min_length is None or min_length < length
    less_max = max_length is None or length < max_length
    return grater_min and less_max


def file_is_hidden(file: str):
    return file.startswith('.')
