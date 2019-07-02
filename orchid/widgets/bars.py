from sys import exit
from PyQt5.QtCore import QUrl, pyqtSignal, QDir
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QSizePolicy, QLineEdit, QStyle, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QPaintEvent
from orchid.widgets.web import WebPage


class SearchBar(QToolBar):
    """
    A widget that contains navigation buttons and a search bar for file and web access.
    """

    signal_return_pressed = pyqtSignal(QUrl)
    signal_webpage_action = pyqtSignal(WebPage.WebAction)
    signal_browser_home_pressed = pyqtSignal(QUrl)
    signal_file_home_pressed = pyqtSignal(QUrl)

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget and fills it buttons and a search bar.

        :param parent: An optional parent object for this toolbar.
        :type parent: QWidget
        """
        super().__init__(parent)
        tr = self.tr

        self._webactions = {}
        self._percent = 0

        # Configure tool bar.
        self.setMovable(False)

        # Back button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go back"))
        button.setProperty("action", WebPage.Back)
        button.pressed.connect(self._on_action_button_pressed)
        self.addWidget(button)
        self._webactions[WebPage.Back] = button

        # Forward button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go forward"))
        button.setProperty("action", WebPage.Forward)
        button.pressed.connect(self._on_action_button_pressed)
        self.addWidget(button)
        self._webactions[WebPage.Forward] = button

        # Stop/reload button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Refresh page"))
        button.setProperty("action", WebPage.Reload)
        button.pressed.connect(self._on_action_button_pressed)
        self.addWidget(button)
        self._webactions[WebPage.Reload] = button
        self._webactions[WebPage.Stop] = button

        # Browser home button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go to your homepage"))
        button.pressed.connect(self._on_browser_home_pressed)
        self.addWidget(button)

        # Search bar.
        self._search_bar = QLineEdit(self)
        self._search_bar.setPlaceholderText(tr("Search for anything"))
        self._search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self._search_bar.setClearButtonEnabled(True)
        self._search_bar.returnPressed.connect(self._on_return_pressed)
        self.addWidget(self._search_bar)

        # File home button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go to your home folder"))
        button.pressed.connect(self._on_file_home_pressed)
        self.addWidget(button)

        # Trash button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setPopupMode(QToolButton.InstantPopup)
        button.setToolTip(tr("Go to your trash"))
        self.addWidget(button)

        # Trash button menu.
        menu = QMenu(button)
        action = QAction(tr("Empty Trash"), menu)
        action.triggered.connect(self._on_empty_trash_pressed)
        action.setToolTip(tr("Delete all items in the trash"))
        menu.addAction(action)
        button.setMenu(menu)

        # Power button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setPopupMode(QToolButton.InstantPopup)
        button.setToolTip(tr("Power options"))
        self.addWidget(button)

        # Power button menu.
        menu = QMenu(button)
        action = QAction(tr("Shut Down"), menu)
        action.triggered.connect(self._on_shutdown_pressed)
        action.setToolTip(tr("Turn off the PC"))
        menu.addAction(action)
        button.setMenu(menu)

    def set_url(self, url: QUrl) -> None:
        """
        Shows the given :class:`QUrl` in the search bar.

        :param url: The URL to show in the search bar.
        :type url: QUrl
        """
        self._search_bar.setText(url.toDisplayString())

    def set_webaction_state(self, webaction: WebPage.WebAction, state: bool) -> None:
        """
        Called whenever a :class:`WebPage.WebAction` like reload or back changes state.

        :param webaction: The :class:`WebPage.WebAction` whose state changed.
        :type webaction: WebPage.WebAction
        :param state: The new state of the webaction; true is enabled, false is disabled.
        :type state: bool
        """
        button = self._webactions.get(webaction, None)
        if isinstance(button, QToolButton):
            button.setEnabled(state)
            if state:
                if webaction == WebPage.Reload:
                    # Show the reload icon since reload is now enabled.
                    button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
                    button.setToolTip(self.tr("Refresh page"))
                    button.setProperty("action", WebPage.Reload)
                elif webaction == WebPage.Stop:
                    # Show the stop icon since stop is now enabled.
                    button.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
                    button.setToolTip(self.tr("Stop loading page"))
                    button.setProperty("action", WebPage.Stop)

    def set_load_progress(self, progress: int) -> None:
        """
        Shows the current load percentage in the search bar.

        :param progress: The current page load percentage.
        :type progress: int
        """
        self._percent = progress

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        # TODO: Color portion of line edit equal to amount of page loaded.

    def _on_action_button_pressed(self) -> None:
        """
        Called whenever an action button is pressed. The sender's "action" property will hold the type of webaction to
        send to the :class:`WebPage` based on which button was pressed.
        """
        webaction = self.sender().property("action")
        if webaction is not None:
            self.signal_webpage_action.emit(webaction)

    def _on_browser_home_pressed(self) -> None:
        """
        Returns the current tab to the user's home page.
        """
        # TODO: Use user settings home path page here.
        self.signal_browser_home_pressed.emit(QUrl("http://www.google.com"))

    def _on_file_home_pressed(self) -> None:
        """
        Returns the current tab to the user's home folder.
        """
        # TODO: Use user settings home path here.
        # TODO: Change the type of widget in the tab to something that views files.
        self.signal_browser_home_pressed.emit(QUrl(QDir.homePath()))

    def _on_return_pressed(self) -> None:
        """
        Signals that return was pressed with the :class:`QUrl` from the search bar at the time of the press.
        """
        url = QUrl.fromUserInput(self._search_bar.text())
        if url is not None:
            self.signal_return_pressed.emit(url)

    def _on_empty_trash_pressed(self) -> None:
        """
        Called when the user presses the "empty trash" menu item. This prompts for confirmation and then deletes all
        files and folders in the trash once given the okay.
        """
        reply = QMessageBox.question(self, self.tr("Confirm"), self.tr("Delete all trash?"))
        if reply == QMessageBox.Yes:
            # TODO: Delete the trash.
            pass

    def _on_shutdown_pressed(self) -> None:
        """
        Called when the user pressed the "shut down" menu item. This prompts for confirmation and then shuts down the
        system once given the okay.
        """
        # TODO: Enable this check again.
        #reply = QMessageBox.question(self, self.tr("Confirm"), self.tr("Shut down now?"))
        #if reply == QMessageBox.Yes:
        exit(0)


class BookmarksBar(QToolBar):
    """
    A widget that contains bookmark buttons for quick access to folder and websites.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget.

        :param parent: An optional parent object for this toolbar.
        :type parent: QWidget
        """
        super().__init__(parent)
        tr = self.tr

        # Configure tool bar.
        self.setMovable(False)

        button = QToolButton(self)
        button.setText(tr("google.com"))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.addWidget(button)


class SideBar(QToolBar):
    """
    A widget that contains options and settings icons for the user to customize.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget.

        :param parent: An optional parent object for this toolbar.
        :type parent: QWidget
        """
        super().__init__(parent)

        # Configure tool bar.
        self.setMovable(False)

        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.addWidget(button)
