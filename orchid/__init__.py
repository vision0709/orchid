from sys import argv
from logging import basicConfig, DEBUG
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread
from orchid.xsys import WindowManager
from orchid.widgets.areas import ActionArea, SettingsArea
from orchid.utils.theme import Themer


class DesktopEnvironment(QObject):
    """
    The Orchid desktop environment.
    """

    def __init__(self) -> None:
        """
        Creates the :class:`WindowManager`, :class:`ActionArea`, and :class:`SettingsArea`. This also themes the whole
        app based on the theme file and configures the loggers.
        """
        self._app = QApplication(argv)  # Create the Qt app.

        # Configure loggers.
        basicConfig(level=DEBUG)

        # Theme the application.
        Themer().apply_theme()

        # Create the system areas before the window manager so we don't have to worry about it centering them.
        self._action_area = ActionArea()  # Create the top panel.
        self._settings_area = SettingsArea()  # Create the side panel.

        # Create the window manager.
        self._wm_thread = QThread()
        self._wm = WindowManager()
        self._wm.moveToThread(self._wm_thread)
        self._wm_thread.started.connect(self._wm.run)
        self._wm.start()
        self._wm_thread.start()

    def run(self) -> int:
        """
        Startup the environment.
        :return: The exit code of the app.
        :rtype: int
        """
        result = self._app.exec()
        self._wm.stop()
        self._wm_thread.quit()
        self._wm_thread.wait()
        return result
