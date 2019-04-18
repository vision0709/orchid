from typing import Union
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget
from PyQt5.QtCore import Qt
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

    def add_widget(self, widget: QWidget) -> None:
        """
        Adds the given widget to a new tab in the central widget. If the given widget is None this does nothing.
        :param widget: The widget to add to the central widget.
        :type widget: QWidget
        """
        if widget is not None:
            self.get_central_widget().addTab(widget, widget.windowTitle())

    @staticmethod
    def get_central_widget() -> QTabWidget:
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
        DesktopWindow.instance.showFullScreen()


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

        # Create the top search bar.
        search_bar = SearchBar(self)
        self.addToolBar(search_bar)

        # Add next bar on next line.
        self.addToolBarBreak(Qt.TopToolBarArea)

        # Create the top bookmarks bar.
        bookmarks_bar = BookmarksBar(self)
        self.addToolBar(bookmarks_bar)

        # Create the main area apps get drawn in.
        main_widget = QTabWidget(self)
        main_widget.addTab(QWidget(), "Test Tab 1")
        main_widget.addTab(QWidget(), "Test Tab 2")
        self.setCentralWidget(main_widget)

        # Create the side bar.
        settings_area = SideBar(self)
        self.addToolBar(Qt.LeftToolBarArea, settings_area)
