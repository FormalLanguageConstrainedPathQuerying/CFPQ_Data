import os
from functools import reduce


def any_filter_combinator(*filters):
    return reduce(lambda acc, f: lambda x: acc(x) or f(x), filters, lambda _: False)


def all_filter_combinator(*filters):
    return reduce(lambda acc, f: lambda x: acc(x) and f(x), filters, lambda _: True)


def file_has_extension(file, extensions=None):
    return extensions is None or any([file.endswith(ext) for ext in extensions])


def file_has_size(file, left_bound=None, right_bound=None):
    size = os.path.getsize(file) // 10**6
    left = left_bound is None or left_bound < size
    right = right_bound is None or size < right_bound
    return left and right
