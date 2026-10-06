"""Archive size formatting shared by the dataset maintainer tools."""

__all__ = [
    "format_size_mb",
]


def format_size_mb(size_bytes: int) -> str:
    """Format an archive size in megabytes for the docs graph tables.

    One unit (MB, 10**6 bytes) is used for every graph. Values below one
    megabyte keep three decimals so that small archives do not round to
    zero; values from one megabyte up keep two.

    Parameters
    ----------
    size_bytes : int
        The archive size in bytes.

    Examples
    --------
    >>> format_size_mb(2472)
    '0.002'
    >>> format_size_mb(988000)
    '0.988'
    >>> format_size_mb(1021000)
    '1.02'
    >>> format_size_mb(99645647)
    '99.65'

    Returns
    -------
    size : str
        The size in MB: three decimals below 1, two decimals from 1 up.
    """
    mb = size_bytes / 1_000_000
    if mb < 1:
        return f"{mb:.3f}"
    return f"{mb:.2f}"
