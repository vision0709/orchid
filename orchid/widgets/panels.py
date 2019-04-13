from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabBar, QHBoxLayout, QPushButton, QSizePolicy, QLineEdit, QStyle


class TabPanel(QTabBar):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setExpanding(False)

        self.addTab("XClock")
        self.addTab("Test Tab 1")


class OmniPanel(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)

        # Back button.
        button = QPushButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(button)

        # Forward button.
        button = QPushButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(button)

        # Home button.
        button = QPushButton(self)
        button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(button)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for anything")
        self.search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        layout.addWidget(self.search_bar)


class BookmarksPanel(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        button = QPushButton("google.com", self)
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(button)
