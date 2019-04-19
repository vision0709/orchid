from PyQt5.QtCore import QObject
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineView, QWebEnginePage


class WebProfile:
    """
    Settings and options shared by all web pages.
    """

    instance = None

    def __init__(self, parent: QObject = None) -> None:
        """
        Initialize the profile singleton.

        :param parent: An optional parent :class:`QObject`
        :type parent: QObject
        """
        if not WebProfile.instance:
            WebProfile.instance = _WebProfile(parent)


class _WebProfile(QWebEngineProfile):
    """
    Settings and options shared by all web pages. This is a singleton.
    """

    def __init__(self, parent: QObject = None) -> None:
        """
        Creates the :class:`_WebProfile`.

        :param parent: An optional parent :class:`QObject`
        :type parent: QObject
        """
        super().__init__(parent)


class WebPage(QWebEnginePage):
    """

    """

    def __init__(self) -> None:
        """

        """
        pass


class WebView(QWebEngineView):
    """

    """

    def __init__(self) -> None:
        """

        """
        pass
