from json import load
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPalette
from orchid.io import FileManager


class Themer:
    """
    A theme manager for :module:`orchid`.
    """

    instance = None

    def __init__(self) -> None:
        """
        Initializes the singleton if it does not already exist.
        """
        if not Themer.instance:
            Themer.instance = _Themer()
        self.color_roles = [QPalette.Window, QPalette.WindowText, QPalette.Base, QPalette.AlternateBase, QPalette.Text,
                            QPalette.BrightText, QPalette.Button, QPalette.ButtonText, QPalette.ToolTipBase,
                            QPalette.ToolTipText, QPalette.Light, QPalette.Midlight, QPalette.Mid, QPalette.Dark,
                            QPalette.Shadow, QPalette.Highlight, QPalette.HighlightedText, QPalette.Link,
                            QPalette.LinkVisited]

    def apply_theme(self) -> None:
        """
        Colors all the widgets of the app according to the current theme.
        """
        palette = QPalette()
        for role in self.color_roles:
            palette.setColor(role, Themer.instance.colors[role])  # Set each role to its corresponding color.
        QApplication.setPalette(palette)


class _Themer:
    """
    Contains the real workings of the :class:`Themer` and is used to ensure only one :class:`Themer` can exist.
    This is a singleton.
    """

    def __init__(self) -> None:
        """
        Loads the theme from a file.
        """
        with open(FileManager().get_theme_file(), "r") as file:
            json_doc = load(file)
        self.colors = {QPalette.Window: QColor(json_doc["colors"]["window"]),
                       QPalette.WindowText: QColor(json_doc["colors"]["windowtext"]),
                       QPalette.Base: QColor(json_doc["colors"]["base"]),
                       QPalette.AlternateBase: QColor(json_doc["colors"]["altbase"]),
                       QPalette.Text: QColor(json_doc["colors"]["text"]),
                       QPalette.BrightText: QColor(json_doc["colors"]["brighttext"]),
                       QPalette.Button: QColor(json_doc["colors"]["button"]),
                       QPalette.ButtonText: QColor(json_doc["colors"]["buttontext"]),
                       QPalette.ToolTipBase: QColor(json_doc["colors"]["tooltipbase"]),
                       QPalette.ToolTipText: QColor(json_doc["colors"]["tooltiptext"]),
                       QPalette.Light: QColor(json_doc["colors"]["light"]),
                       QPalette.Midlight: QColor(json_doc["colors"]["midlight"]),
                       QPalette.Mid: QColor(json_doc["colors"]["mid"]),
                       QPalette.Dark: QColor(json_doc["colors"]["dark"]),
                       QPalette.Shadow: QColor(json_doc["colors"]["shadow"]),
                       QPalette.Highlight: QColor(json_doc["colors"]["highlight"]),
                       QPalette.HighlightedText: QColor(json_doc["colors"]["highlightedtext"]),
                       QPalette.Link: QColor(json_doc["colors"]["link"]),
                       QPalette.LinkVisited: QColor(json_doc["colors"]["linkvisited"])}
