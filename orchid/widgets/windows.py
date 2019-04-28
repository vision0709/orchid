from typing import Union
from PyQt5.QtCore import Qt, QUrl, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QTabBar, QLineEdit, QAction, QSizePolicy, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from orchid.widgets.bars import SearchBar, BookmarksBar, SideBar
from orchid.widgets.web import WebView, WebPage


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

    def add_tab(self, widget: QWidget, title: str = None) -> None:
        """
        Adds the given widget to a new tab in the central widget. If the given widget is None this does nothing.

        :param widget: The widget to add to the central widget.
        :type widget: QWidget
        :param title: An optional string to add as the new tab's title text.
        :type title: str
        """
        # Do nothing if no widget was given.
        if widget is not None:
            central_widget = self.get_central_widget()  # Get the central tab widget.

            # Connect to page loading signals if the widget is a web view.
            if isinstance(widget, QWebEngineView):
                widget.loadProgress.connect(self._on_load_progress_changed)
                widget.loadFinished.connect(self._on_load_progress_finished)

            # Set an appropriate title.
            if not title and not widget.windowTitle():
                title = self.tr("Untitled")
            else:
                title = widget.windowTitle()

            central_widget.addTab(widget, title)  # Add the widget to a new tab.

    def add_background_tab(self) -> None:
        """"""

    @staticmethod
    def get_central_widget() -> QTabWidget:
        """
        Returns the app area widget where apps, folder, and web pages are drawn.

        :return: The widget that contains all app, folder, and web page widgets.
        :rtype: QTabWidget
        """
        return DesktopWindow.instance.centralWidget()

    def _on_load_progress_changed(self, progress: int) -> None:
        print("Loading:", progress)

    def _on_load_progress_finished(self, status: bool) -> None:
        print("Loaded:", status)

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
        main_widget.setDocumentMode(True)  # Draw the tab widget suitable for documents.
        main_widget.setElideMode(Qt.ElideRight)  # Let tabs overflow the right side of the tab bar.
        self.setCentralWidget(main_widget)

        # Configure the main widget's tab bar.
        tab_bar = main_widget.tabBar()
        tab_bar.setMovable(True)
        tab_bar.setTabsClosable(True)
        tab_bar.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)

        # Create the side bar.
        settings_area = SideBar(self)
        self.addToolBar(Qt.LeftToolBarArea, settings_area)


class PopupWindow(QWidget):
    """
    A :class:`QWidget` popup to display a :class:`WebPage`'s request for a new popup window.
    """

    def __init__(self, profile: QWebEngineProfile) -> None:
        """
        Creates the :class:`PopupWindow`, initializes its web view, action, and URL, and listens for changes in the
        children of the popup.

        :param profile:
        """
        super().__init__()

        # Configure the popup.
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add a layout to the popup.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create the popup's action.
        action = QAction(self)

        # Create the URL text box.
        self._url_text_box = QLineEdit(self)
        self._url_text_box.setReadOnly(True)
        self._url_text_box.addAction(action, QLineEdit.LeadingPosition)
        layout.addWidget(self._url_text_box)

        # Create the web view.
        self._web_view = WebView(self)
        self._web_view.setPage(WebPage(profile, self._web_view))
        layout.addWidget(self._web_view)

        self._web_view.setFocus()

        # Listen for signals from the popup's widgets.
        self._web_view.titleChanged.connect(self.setWindowTitle)
        self._web_view.urlChanged.connect(self._on_url_changed)
        self._web_view.signal_favicon_changed(action.setIcon)
        self._web_view.page().geometryChangeRequested.connect(self._on_geometry_change_requested)
        self._web_view.page().windowCloseRequested.connect(self.close)

    def _on_url_changed(self, url: QUrl) -> None:
        """
        Shows the given :class:`QUrl` in the text box of this :class:`PopupWindow`.

        :param url: The :class:`QUrl` to show in the popup.
        :type url: QUrl
        """
        self._url_text_box.setText(url.toDisplayString())

    def _on_geometry_change_requested(self, geometry: QRect) -> None:
        """
        Updates this window's geometry whenever the child page's geometry updates.

        :param geometry: The new geometry to update the :class:`PopupWindow` with.
        :type geometry: QRect
        """
        window = self.windowHandle()
        if window is not None:
            self.setGeometry(geometry.marginsRemoved(window.frameMargins()))
        self.show()
        self._web_view.setFocus()

    def get_web_view(self) -> WebView:
        """
        Returns this :class:`PopupWindow`'s :class:`WebView`.

        :return: The :class:`WebView` for this :class:`PopupWindow`.
        :rtype: WebView
        """
        return self._web_view
