import logging
import os
import shutil
from typing import List, Union

from core.entry import Entry
from util import environment

logger = logging.getLogger(__name__)


class Register:
    def __init__(self, number: int):
        self.name = "register" + str(number)
        self._path = os.path.join(environment.buffer, self.name)

    def copy_to(self, src: Union[List[Entry], Entry]):
        """
        Writes given entries or given entry to this register
        """
        def write_single_entry(entry: Entry):
            logger.info(f"Yanking {entry.name} to {self.name}")
            copy(entry.path, os.path.join(self.path, entry.name))

        self.clear()
        if type(src) is list:
            for entry in src:
                write_single_entry(entry)
        else:
            write_single_entry(src)

    def move_to(self, entry: Entry):
        self.clear()
        src = entry.path
        dest = os.path.join(self.path, entry.name)
        logger.info(f"Moving {src} to {dest}")
        os.rename(src, dest)

    def read_from(self, target: Entry):
        """
        Copies this registers content into given target dir
        """
        for file in os.listdir(self.path):
            src = os.path.join(self.path, file)
            dest = os.path.join(target.path, file)
            logger.info(f"Pasting {self.name} to {dest}")
            copy(src, dest)

    def clear(self):
        for file in os.listdir(self.path):
            path = os.path.join(self.path, file)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    @property
    def path(self):
        os.makedirs(self._path, exist_ok=True)
        return self._path


registers = [Register(x) for x in range(10)]


def copy(src: str, dest: str):
    """
    Recursively copy src to dest
    :param src:
    :param dest:
    :return:
    """
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy(src, dest)
    except OSError as e:
        logger.error(f"Failed to yank dir. Error: {e}")
