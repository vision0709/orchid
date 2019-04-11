from sys import argv
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, QRect
from orchid.anther import WindowManager
from orchid.sepal import ActionArea, SettingsArea


class DesktopEnvironment(QObject):
    """
    The Orchid desktop environment.
    """

    def __init__(self) -> None:
        """
        Creates the WindowManager, ActionArea, and SettingsArea.
        """
        self._app = QApplication(argv)

        # Create the window manager.
        self._wm_thread = QThread()
        self._wm = WindowManager()
        self._wm.moveToThread(self._wm_thread)
        self._wm_thread.started.connect(self._wm.run)
        self._wm.start()
        self._wm_thread.start()

        # Give the window manager time to start up.
        sleep(1)

        # Create the top panel.
        self._top_panel = ActionArea()
        self._top_panel.setGeometry(QRect(0, 0, self._wm.get_screen_width(), self._wm.get_screen_height() * .08))
        self._top_panel.show()

        # Create the side panel.
        self._side_panel = SettingsArea()
        self._side_panel.setGeometry(QRect(0, self._wm.get_screen_height() * .03, self._wm.get_screen_width() * .03, self._wm.get_screen_height()))
        self._side_panel.show()

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
