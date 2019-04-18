from os import mkdir
from os.path import exists, join, dirname
from pathlib import Path


class FileManager:
    """
    A manager of all files in and out of :module:`orchid`.
    """

    instance = None

    def __init__(self) -> None:
        """
        Creates the instance of the :class:`_FileManager` if it does not already exist.
        """
        if not FileManager.instance:
            FileManager.instance = _FileManager()

    def get_theme_file(self) -> str:
        """
        Returns an absolute path to the theme file to use for theming the app.

        :return: The path to the theme file.
        :rtype: str
        """
        return FileManager.instance.theme_file


class _FileManager:
    """
    Contains the functionality of the :class:`FileManager` and is used to ensure on one :class:`FileManager`
    exists. This is a singleton.
    """

    def __init__(self) -> None:
        """
        Verifies and creates all of the files for :module:`orchid`.
        """
        self.theme_file = join(Path.home(), ".orchid", "themes", "default.json")

        if not exists(dirname(self.theme_file)):
            mkdir(dirname(self.theme_file))
            # TODO: Copy theme file into directory.
        elif not exists(self.theme_file):
            # TODO: Copy theme file into directory.
            pass
