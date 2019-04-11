from PyQt5.QtWidgets import QWidget, QVBoxLayout


class ActionArea(QWidget):
    """
    A central widget that expands as wide as possible and contains a :py:class:`TabPanel`, :py:class:`OmniPanel`, and
    :py:class:`BookmarksPanel`.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget and all of its children.

        :param parent: An optional parent object for this panel.
        :type parent: QWidget
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(TabPanel(self))
        layout.addWidget(OmniPanel(self))
        layout.addWidget(BookmarksPanel(self))
        self.setLayout(layout)


class SettingsArea(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)


class TabPanel(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)


class OmniPanel(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)


class BookmarksPanel(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
