import os
import shutil
from pathlib import Path
from typing import List

from cfpq_data.config import MAIN_FOLDER


def __unpack_archive_listdir(target_dir: Path, arch: str) -> List[str]:
    """
    Returns a list of files from the archive

    :param target_dir: folder where the archive will be unpacked
    :type target_dir: Path
    :param arch: path to archive
    :type arch: str
    :return: list of files from the archive
    :rtype: List[str]
    """

    tmp = target_dir / 'tmp'
    os.mkdir(tmp)
    shutil.unpack_archive(arch, tmp)
    result = os.listdir(tmp)
    shutil.rmtree(tmp)
    return result


def unpack_graph(graph_group: str, graph_name: str) -> str:
    """
    Unpacks the graph to the desired folder

    :param graph_group: graph group type
    :type graph_group: str
    :param graph_name: graph name
    :type graph_name: str
    :return: path to the unpacked graph
    :rtype: str
    """

    to = MAIN_FOLDER / 'data' / graph_group / 'Graphs'

    arch = to / f'{graph_name}.tar.xz'

    shutil.unpack_archive(arch, to)

    graph = __unpack_archive_listdir(to, arch)[0]

    os.remove(arch)

    return os.path.join(to, graph)


def clean_dir(name: str) -> None:
    """
    Clears the specified folder

    :param name: folder to clear
    :type name: str
    :return: None
    :rtype: None
    """

    path = MAIN_FOLDER / 'data' / name / 'Graphs'
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def add_graph_dir(name: str) -> Path:
    """
    Creates a folder for the specified graph type

    :param name: specified graph type
    :type name: str
    :return: path to folder for the specified graph type
    :rtype: Path
    """

    dst = MAIN_FOLDER / 'data' / name / 'Graphs'
    dst.mkdir(parents=True, exist_ok=True)
    return dst
