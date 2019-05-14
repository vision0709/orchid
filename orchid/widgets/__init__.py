from logging import getLogger
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QPoint
from PyQt5.QtGui import QIcon, QKeySequence, QCursor
from PyQt5.QtWidgets import QWidget, QTabWidget, QTabBar, QMenu, QToolButton
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from orchid.widgets.web import WebView, WebPage


class LogWidget(QWidget):
    """
    A normal :class:`QWidget` with a logger built in.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates a widget with a logger.

        :param parent: The QWidget parent of this widget. Parenting ensures children widgets are destroyed when a parent
         is destroyed.
        :type parent: QWidget
        """
        super().__init__(parent)
        self._logger = getLogger(__name__)


class TabWidget(QTabWidget):
    """
    The main widget in :module:`orchid`. This is the tab widget that displays all other windows.
    """

    # Class signals.
    signal_link_hovered = pyqtSignal(str)
    signal_load_progress_changed = pyqtSignal(int)
    signal_title_changed = pyqtSignal(str)
    signal_url_changed = pyqtSignal(QUrl)
    signal_favicon_changed = pyqtSignal(QIcon)
    signal_webaction_state_changed = pyqtSignal(WebPage.WebAction,  bool)
    signal_dev_tools_requested = pyqtSignal(WebPage)

    def __init__(self, profile: QWebEngineProfile, parent: QWidget = None) -> None:
        """
        Creates the tab widget and listens for changes in its tab bar.

        :param profile: The :class:`QWebEngineProfile` to use for this :class:`TabWidget`.
        :type profile: QWebEngineProfile
        :param parent: An optional parent widget of this tab widget.
        :type parent: QWidget
        """
        super().__init__(parent)

        # Configure tab widget.
        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)  # Which side of the tab bar to overflow.
        self.currentChanged.connect(self._on_current_tab_changed)

        self._profile = profile
        self._logger = getLogger(__name__)

        # Configure the tab bar.
        tab_bar = self.tabBar()
        tab_bar.setTabsClosable(True)
        tab_bar.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)
        tab_bar.setMovable(True)
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)

        # Listen for tab bar changes.
        tab_bar.customContextMenuRequested.connect(self._on_context_menu_requested)
        tab_bar.tabCloseRequested.connect(self.close_tab)

        # Listen for tab changes.
        self.currentChanged.connect(self._on_current_tab_changed)

        # Handle private tabs.
        if profile.isOffTheRecord():
            # TODO: Show incognito icon on tab bar maybe.
            pass

        # Add the new tab button.
        index = self.addTab(QWidget(self), "")  # Create an empty new tab for the button to sit on.
        new_tab_button = QToolButton(tab_bar)
        new_tab_button.setText("+")
        new_tab_button.setToolTip(self.tr("Creates a new tab"))
        tab_bar.setTabButton(index, QTabBar.LeftSide, new_tab_button)

    def _on_current_tab_changed(self, index: int) -> None:
        """
        Callback for when the current tab in the :class:`TabWidget` changes. This updates listeners as to the current
        tab's values.

        :param index: The index of the current tab.
        :type index: int
        """
        # Setup tab default values.
        title = ""
        load_progress = 0
        url = QUrl()
        favicon = QIcon()
        back_state = False
        forward_state = False
        stop_state = False
        reload_state = True

        if index >= 0:
            # Make a new web page and focus it.
            view = self.widget(index)  # This should be a WebView.
            if isinstance(view, WebView):
                if not view.url().isEmpty():
                    view.setFocus()

                # Change defaults to new page values.
                title = view.title()
                load_progress = view.get_load_progress()
                url = view.url()
                favicon = view.get_favicon()
                back_state = view.is_webaction_enabled(WebPage.Back)
                forward_state = view.is_webaction_enabled(WebPage.Forward)
                stop_state = view.is_webaction_enabled(WebPage.Stop)
                reload_state = view.is_webaction_enabled(WebPage.Reload)

        # Notify listeners of tab values.
        self.signal_title_changed.emit(title)
        self.signal_load_progress_changed.emit(load_progress)
        self.signal_url_changed.emit(url)
        self.signal_favicon_changed.emit(favicon)
        self.signal_webaction_state_changed.emit(WebPage.WebAction.Back, back_state)
        self.signal_webaction_state_changed.emit(WebPage.WebAction.Forward, forward_state)
        self.signal_webaction_state_changed.emit(WebPage.WebAction.Stop, stop_state)
        self.signal_webaction_state_changed.emit(WebPage.WebAction.Reload, reload_state)

    def _on_context_menu_requested(self, point: QPoint) -> None:
        """
        Creates a right-click context menu at the current cursor position.

        :param point: The :class:`QPoint` where the right-click happened.
        :type point: QPoint
        """
        # Create a new menu with a default "New Tab" action.
        menu = QMenu(self)
        menu.addAction(self.tr("New &Tab"), self.create_tab, QKeySequence.AddTab)

        # Populate the reset of the menu based on if a tab was clicked.
        index = self.tabBar().tabAt(point)
        if index >= 0:
            # A tab was clicked on, add options for it to the menu.
            menu.addAction(self.tr("Clone Tab"), lambda index=index: self.clone_tab(index))
            menu.addSeparator()
            menu.addAction(self.tr("&Close Tab"), lambda index=index: self.close_tab(index), QKeySequence.Close)
            menu.addAction(self.tr("Close &Other Tabs"), lambda index=index: self.close_other_tabs(index))
            menu.addSeparator()
            menu.addAction(self.tr("&Reload Tab"), lambda index=index: self.reload_tab(index), QKeySequence.Refresh)
        else:
            menu.addSeparator()
        menu.addAction(self.tr("Reload All Tabs"), self.reload_all_tabs)

        # Show the new menu.
        menu.exec(QCursor.pos())

    def create_tab(self) -> WebView:
        """
        Creates a new background tab and then sets that background tab to be the current tab.

        :return: The :class:`WebView` created.
        :rtype: WebView
        """
        webview = self.create_background_tab()
        self.setCurrentWidget(webview)
        return webview

    def create_background_tab(self) -> WebView:
        """
        Creates a new tab with a new :class:`WebPage` in a new :class:`WebView`.
        """
        # Create the new WebView and WebPage.
        webview = WebView(self)
        webpage = WebPage(self._profile, webview)
        webview.setPage(webpage)

        # Listen for WebView changes.
        webview.titleChanged.connect(lambda title, webview=webview: self._on_webview_title_changed(title, webview))
        webview.urlChanged.connect(lambda url, webview=webview: self._on_webview_url_changed(url, webview))
        webview.loadProgress.connect(lambda progress, webview=webview: self._on_webview_load_progress_changed(progress, webview))
        webview.signal_favicon_changed.connect(lambda icon, webview=webview: self._on_webview_favicon_changed(icon, webview))
        webview.signal_webaction_state_changed.connect(lambda action, enabled, webview=webview: self._on_webview_webaction_state_changed(action, enabled, webview))
        webview.signal_dev_tools_requested.connect(self.signal_dev_tools_requested)

        # Listen for WebPage changes.
        webpage.linkHovered.connect(lambda url, webview=webview: self._on_webpage_link_hovered(url, webview))
        webpage.windowCloseRequested.connect(lambda webview=webview: self._on_webpage_window_close_requested(webview))

        # Configure the new WebView.
        index = self.addTab(webview, self.tr("(Untitled)"))
        self.setTabIcon(index, webview.get_favicon())
        webview.resize(self.currentWidget().size())
        webview.show()

        # TODO: Use user defaults for a homepage.
        webpage.setUrl(QUrl("https://www.google.com"))

        return webview

    def _on_webview_title_changed(self, title: str, webview: WebView) -> None:
        """
        Updates the tab's title and tooltip text with the given title.

        :param title: The new title for this tab.
        :type title: str
        :param webview: The :class:`WebView` whose title was changed.
        :type webview: WebView
        """
        index = self.indexOf(webview)

        # Update the tab text if this widget has a tab.
        if index >= 0:
            self.setTabText(index, title)
            self.setTabToolTip(index, title)

        # Notify listeners of a title change if this widget is the current widget.
        if index == self.currentIndex():
            self.signal_title_changed.emit(title)

    def _on_webview_url_changed(self, url: QUrl, webview: WebView) -> None:
        """
        Updates the tab with the given :class:`QUrl`.

        :param url: The :class:`QUrl` the :class:`WebView` was changed to.
        :type url: QUrl
        :param webview: The :class:`WebView` that had its URL changed.
        :type webview: WebView
        """
        index = self.indexOf(webview)

        # Update the tab data with the new URL.
        if index >= 0:
            self.tabBar().setTabData(index, url)

        # Notify listeners of the URL change.
        if index == self.currentIndex():
            self.signal_url_changed.emit(url)

    def _on_webview_load_progress_changed(self, progress: int, webview: WebView) -> None:
        """
        Notifies listeners that the load progress percentage has changed.

        :param progress: The load progress in percent out of 100.
        :type progress: int
        :param webview: The :class:`WebView` whose load progress has changed.
        :type webview: WebView
        """
        if self.currentIndex() == self.indexOf(webview):
            self.signal_load_progress_changed.emit(progress)

    def _on_webview_favicon_changed(self, icon: QIcon, webview: WebView) -> None:
        """
        Notifies listeners that the :class:`QIcon` of this tab has been changed.

        :param icon: The new :class:`QIcon` for this tab.
        :type icon: QIcon
        :param webview: The :class:`WebView` whose icon just changed.
        :type webview: WebView
        """
        index = self.indexOf(webview)

        # Update this tab's icon with the new icon.
        if index >= 0:
            self.setTabIcon(index, icon)

        # Notify listeners of the icon change.
        if self.currentIndex() == index:
            self.signal_favicon_changed.emit(icon)

    def _on_webview_webaction_state_changed(self, webaction: WebPage.WebAction, enabled: bool, webview: WebView) -> None:
        """
        Notifies listeners of state changes in the given :class:`WebPage.WebAction`.

        :param webaction: The action that was changed.
        :type webaction: WebPage.WebAction
        :param enabled: The current state of the action. If this is False then the action is disabled.
        :type enabled: bool
        :param webview: The :class:`WebView` whose :class:`WebPage` has an action whose state has changed.
        :type webview: WebView
        """
        if self.currentIndex() == self.indexOf(webview):
            self.signal_webaction_state_changed.emit(webaction, enabled)

    def _on_webpage_link_hovered(self, url: str, webview: WebView) -> None:
        """
        Notifies listeners when a :class:`WebPage` has a hyperlink that is being hovered over by the mouse.

        :param url: The URL of the hyperlink that is being hovered as a string.
        :type url: str
        :param webview: The :class:`WebView` whose link is being hovered over.
        :type webview: WebView
        """
        if self.currentIndex() == self.indexOf(webview):
            self.signal_link_hovered.emit(url)

    def _on_webpage_window_close_requested(self, webview: WebView) -> None:
        """
        Closes the tab containing the given :class:`WebView`.

        :param webview: The :class:`WebView` whose tab is being closed.
        :type webview: WebView
        """
        index = self.indexOf(webview)
        if index >= 0:
            self.close_tab(index)

    def reload_all_tabs(self) -> None:
        """
        Calls :method:`reload()` method of each :class:`WebView` in this :class:`TabWidget`.
        """
        for i in range(self.count()):
            widget = self.widget(i)
            if isinstance(widget, WebView):
                widget.reload()

    def close_other_tabs(self, index: int = 0) -> None:
        """
        Closes all tabs except for the one found at the given index. If no index is given, closes all tabs but the
        first tab.

        :param index: The location of the tab to not close.
        :type index: int
        """
        for i in range(self.count() - 1, index, -1):
            self.close_tab(i)
        for i in range(index - 1, -1, -1):
            self.close_tab(i)

    def close_tab(self, index: int = 0) -> None:
        """
        Closes the tab found at the given index. If no index is specified then the first tab is removed.

        :param index: The index of the tab to close.
        :type index: int
        """
        widget = self.widget(index)
        if isinstance(widget, WebView):
            # Check if the widget has focus before removing it.
            has_focus = widget.hasFocus()
            self.removeTab(index)
            widget.deleteLater()

            # Focus the next widget if the one that was removed had focus.
            if has_focus and self.count() > 0:
                self.currentWidget().setFocus()

            # Make a new tab if the last tab was removed.
            if self.count() == 0:
                self.create_tab()
        else:
            self._logger.warning("Cannot close a tab that is not a WebView")

    def clone_tab(self, index: int = 0) -> None:
        """
        Clones the given tab. If no index is specified then the first tab is cloned.

        :param index: The index of the tab to clone.
        :type index: int
        """
        widget = self.widget(index)
        if isinstance(widget, WebView):
            new_tab = self.create_tab()
            new_tab.setUrl(widget.url())
        else:
            self._logger.warning("Cannot clone a tab that is not a WebView")

    def set_url(self, url: QUrl) -> None:
        """
        Sets the current tab's URL to the given :class:`QUrl`.

        :param url: The URL to navigate the current tab to.
        :type url: QUrl
        """
        widget = self.currentWidget()
        if isinstance(widget, WebView):
            widget.setUrl(url)
            widget.setFocus()
        else:
            self._logger.warning("Cannot set a URL on a tab that is not a WebView")

    def trigger_webpage_action(self, webaction: WebPage.WebAction) -> None:
        """
        Triggers the given :class:`WebAction` on the current tab's :class:`WebView`.

        :param webaction: The :class:`WebAction` to trigger.
        :type webaction: WebPage.WebAction
        """
        widget = self.currentWidget()
        if isinstance(widget, WebView):
            widget.triggerPageAction(webaction)
            widget.setFocus()

    def next_tab(self) -> None:
        """
        Changes this widget's view to the next tab.
        """
        next_index = self.currentIndex() + 1
        if next_index == self.count():
            next_index = 0
        self.setCurrentIndex(next_index)

    def previous_tab(self) -> None:
        """
        Changes this widget's view to the previous tab.
        """
        previous_index = self.currentIndex() - 1
        if previous_index < 0:
            previous_index = self.count() - 1
        self.setCurrentIndex(previous_index)

    def reload_tab(self, index: int = 0) -> None:
        """
        Reloads the tab found at the specified index.

        :param index: The index of the tab to reload.
        :type index: int
        """
        widget = self.widget(index)
        if isinstance(widget, WebView):
            widget.reload()
