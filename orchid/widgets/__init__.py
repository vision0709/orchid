from logging import getLogger
from PyQt5.QtWidgets import QWidget


class Constants:
    """
    Constant values commonly used in :module:`widgets`.
    """
    PERCENT_WIDTH = .03
    PERCENT_HEIGHT = .08


class LogWidget(QWidget):
    """
    A normal :class:`QWidget` with a logger already in it.
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