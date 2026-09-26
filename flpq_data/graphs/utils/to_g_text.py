"""Generate FastMatrixCFPQ .g graph files from MatrixMarket archives."""

import logging
import pathlib
import re
from typing import Union

__all__ = ["graph_dir_to_g_text"]

_INDEXED_RE = re.compile(r"^(.+)_(\d+)$")


def _reverse_label(label: str) -> str:
    if label.endswith("_i"):
        return label[:-2] + "_r_i"
    return label + "_r"


def graph_dir_to_g_text(
    path: Union[pathlib.Path, str],
) -> str:
    """Generates a FastMatrixCFPQ .g file text from a directory of mtx files.

    Each ``*.mtx`` file contributes forward edges; reverse edges are
    auto-generated with the :func:`reverse_label` convention. Indexed files
    (``X_N.mtx``) produce 4-column lines with label ``X_i`` and index ``N``.

    Parameters
    ----------
    path : Union[Path, str]
        Directory containing MatrixMarket files.

    Examples
    --------
    >>> import pathlib, tempfile
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> _ = (d / "a.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 1\\n0 1\\n"
    ... )
    >>> _ = (d / "b_5.mtx").write_text(
    ...     "%%MatrixMarket matrix coordinate pattern general\\n"
    ...     "%%GraphBLAS type bool\\n3 3 1\\n2 0\\n"
    ... )
    >>> text = graph_dir_to_g_text(d)
    >>> lines = text.strip().splitlines()
    >>> len(lines)
    4
    >>> "0 1 a" in lines
    True
    >>> "1 0 a_r" in lines
    True
    >>> "2 0 b_i 5" in lines
    True
    >>> "0 2 b_r_i 5" in lines
    True

    Returns
    -------
    text : str
        The .g file content.
    """
    path = pathlib.Path(path)
    g_lines: list[str] = []

    for mtx_file in sorted(path.glob("*.mtx")):
        label_base = mtx_file.stem
        m = _INDEXED_RE.match(label_base)
        if m:
            base, idx = m.group(1), m.group(2)
            label = f"{base}_i"
            has_index = True
        else:
            label, idx = label_base, ""
            has_index = False

        rev = _reverse_label(label)

        with open(mtx_file, "r") as f:
            lines = f.readlines()

        idx_line = 1
        while idx_line < len(lines) and lines[idx_line].startswith("%"):
            idx_line += 1
        header = lines[idx_line].split()
        idx_line += 1
        n_entries = int(header[2])

        for line in lines[idx_line : idx_line + n_entries]:
            parts = line.split()
            u, v = int(parts[0]), int(parts[1])
            if has_index:
                g_lines.append(f"{u} {v} {label} {idx}")
                g_lines.append(f"{v} {u} {rev} {idx}")
            else:
                g_lines.append(f"{u} {v} {label}")
                g_lines.append(f"{v} {u} {rev}")

    text = "\n".join(g_lines) + "\n" if g_lines else ""

    logging.info(f"Generate .g text from {path=}: {len(g_lines)} edges")

    return text
