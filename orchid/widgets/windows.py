from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from orchid.widgets import TabWidget
from orchid.widgets.bars import SearchBar, BookmarksBar, SideBar


class DesktopWindow:
    """
    The root window of all other windows in :module:`orchid`. This is a :class:`QMainWindow` that holds all other UI.
    """

    instance = None

    def __init__(self, parent: QWidget = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()) -> None:
        """
        Create an instance of the :class:`_DesktopWindow` if one does not already exist.

        :param parent: An optional :class:`QWidget` parent object.
        :type parent: QWidget
        :param flags: Optional :class:`Qt.WindowFlags` or :class:`Qt.WindowType`s that define how the window is
        displayed.
        :type flags: Union[Qt.WindowFlags, Qt.WindowType]
        """
        if not DesktopWindow.instance:
            DesktopWindow.instance = _DesktopWindow(parent, flags)
            self.tr = DesktopWindow.instance.tr

    @staticmethod
    def get_tab_widget() -> TabWidget:
        """
        Returns the app area widget where apps, folder, and web pages are drawn.

        :return: The widget that contains all app, folder, and web page widgets.
        :rtype: QTabWidget
        """
        return DesktopWindow.instance.centralWidget()

    @staticmethod
    def show() -> None:
        """
        Make the :class:`DesktopWindow` visible and fullscreen.
        """
        #DesktopWindow.instance.showFullScreen()
        DesktopWindow.instance.show()


class _DesktopWindow(QMainWindow):
    """
    Contains the real workings of the :class:`DesktopWidget` and is used to ensure only one :class:`DesktopWidget` can
    exist. This is a singleton.
    """

    def __init__(self, parent: QWidget = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()) -> None:
        """
        Creates the action, settings, status, and window areas of the desktop.

        :param parent: An optional :class:`QWidget` parent object.
        :type parent: QWidget
        :param flags: Optional :class:`Qt.WindowFlags` or :class:`Qt.WindowType`s that define how the window is
        displayed.
        :type flags: Union[Qt.WindowFlags, Qt.WindowType]
        """
        super().__init__(parent, flags)

        # Configure the main window.
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # Create the main area apps get drawn in.
        central_widget = TabWidget(QWebEngineProfile.defaultProfile(), self)
        central_widget.create_tab()
        self.setCentralWidget(central_widget)

        # Connect to signals from the central widget.
        if not for_dev_tools:
            central_widget.signal_link_hovered.connect(self._on_link_hovered)

        # Create the top search bar that will manage the central widget.
        search_bar = SearchBar(central_widget, self)
        self.addToolBar(search_bar)

        # Add next bar on next line.
        self.addToolBarBreak(Qt.TopToolBarArea)

        # Create the top bookmarks bar.
        bookmarks_bar = BookmarksBar(self)
        self.addToolBar(bookmarks_bar)

        # Create the side bar.
        settings_area = SideBar(self)
        self.addToolBar(Qt.LeftToolBarArea, settings_area)

    def _on_link_hovered(self, url: str) -> None:
        """
        Displays the URL of the link being hovered on a :class:`WebPage` in the status bar.

        :param url: The URL of the link that is being hovered.
        :type url: str
        """
        self.statusBar().showMessage(url)
