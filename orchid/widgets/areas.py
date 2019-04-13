from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton, QSizePolicy
from orchid.widgets import Constants
from orchid.widgets.panels import TabPanel, OmniPanel, BookmarksPanel


class ActionArea(QWidget):
    """
    A central widget that expands as wide as possible and contains a :class:`TabPanel`, :class:`OmniPanel`, and
    :class:`BookmarksPanel`.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget and positions it on the screen.

        :param parent: An optional parent object for this panel.
        :type parent: QWidget
        """
        super().__init__(parent)

        # Add children to layout.
        layout = QVBoxLayout(self)
        layout.addWidget(TabPanel(self))
        layout.addWidget(OmniPanel(self))
        layout.addWidget(BookmarksPanel(self))
        self.setLayout(layout)

        # Resize and position the widget on the screen.
        screen_geometry = QApplication.desktop().availableGeometry()
        self.resize(screen_geometry.width(), self.minimumHeight())

        self.show()


class SettingsArea(QWidget):
    """
    A widget that contains options and settings icons for the user to customize.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Creates the widget and positions it on the screen.

        :param parent: An optional parent object for this panel.
        :type parent: QWidget
        """
        super().__init__(parent)

        # Resize and position the widget on the screen.
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(screen_geometry.x(),
                               screen_geometry.height() * Constants.PERCENT_HEIGHT + 20,
                               screen_geometry.width() * Constants.PERCENT_WIDTH,
                               screen_geometry.height() - screen_geometry.height() * Constants.PERCENT_HEIGHT))

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        button = QPushButton("Test", self)
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(button)
        self.setLayout(layout)

        self.show()
