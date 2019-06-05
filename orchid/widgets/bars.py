from sys import exit
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QSizePolicy, QLineEdit, QStyle, QMenu, QAction, QMessageBox
from orchid.widgets import TabWidget
from orchid.widgets.web import WebPage


class SearchBar(QToolBar):
    """
    A widget that contains navigation buttons and a search bar for file and web access.
    """

    def __init__(self, tab_widget: TabWidget, for_dev_tools: bool = False, parent: QWidget = None) -> None:
        """
        Creates the widget and fills it buttons and a search bar.

        :param tab_widget: The :class:`TabWidget` this :class:`SearchBar` will manage.
        :type tab_widget: TabWidget
        :param for_dev_tools:
        :type for_dev_tools: bool
        :param parent: An optional parent object for this toolbar.
        :type parent: QWidget
        """
        super().__init__(parent)
        tr = self.tr

        # Configure tool bar.
        self.setMovable(False)
        self.tab_widget = tab_widget

        # Connect to tab widget changes.
        if not for_dev_tools:
            self.tab_widget.signal_favicon_changed.connect(self._on_favicon_changed)

        # Back button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go back"))
        button.pressed.connect(lambda action=WebPage.Back: self.tab_widget.trigger_webpage_action(action))
        self.addWidget(button)

        # Forward button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go forward"))
        button.pressed.connect(lambda action=WebPage.Forward: self.tab_widget.trigger_webpage_action(action))
        self.addWidget(button)

        # Refresh button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Refresh page"))
        button.pressed.connect(lambda action=WebPage.Reload: self.tab_widget.trigger_webpage_action(action))
        self.addWidget(button)

        # Browser home button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go to your homepage"))
        self.addWidget(button)

        # Search bar.
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText(tr("Search for anything"))
        self.search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.search_bar.setClearButtonEnabled(True)
        self.addWidget(self.search_bar)

        # File home button.
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        button.setToolTip(tr("Go to your home folder"))
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
