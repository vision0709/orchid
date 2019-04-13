from os import environ
from logging import getLogger
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from Xlib.display import Display
from Xlib.X import SubstructureRedirectMask, MapRequest, KeyPress, RevertToParent, CurrentTime, Above
from Xlib.error import ConnectionClosedError, BadAccess


class WindowManager(QObject):
    """
    An X window manager that positions new X clients.
    """

    def __init__(self) -> None:
        """
        Requests resources from the X system.
        """
        super().__init__()
        display_num = environ.get("DISPLAY")
        if not display_num:
            display_num = ":0"

        # Create a logger.
        # TODO: Add a file handler and formatter.
        self._logger = getLogger(__name__)
        self._display = Display(display_num)  # Create the connection to the X server.

        # Take control of window management on the default screen.
        # TODO: Manage more than just the default screen.
        # TODO: Manage more than just the mapping events.
        try:
            self._display.screen().root.change_attributes(event_mask=SubstructureRedirectMask)
        except BadAccess as error:
            print("Access error:", error)

        self.is_running = False

    def start(self) -> None:
        """
        Starts the WindowManager running.
        """
        self.is_running = True

    def stop(self) -> None:
        """
        Stops the WindowManager running,
        """
        self.is_running = False

    def run(self) -> None:
        """
        The main loop of the WindowManager.
        """
        screen_geometry = QApplication.desktop().screenGeometry()

        try:
            while self.is_running:
                if self._display.pending_events() > 0:  # Check if there are any pending events in the queue.
                    event = self._display.next_event()  # Get the next pending event.
                    if event.type == KeyPress:
                        print("Got a key press event!")
                    elif event.type == MapRequest:
                        print("Got a map request event!")
                        x = screen_geometry.center().x() - event.window.get_geometry().width / 2
                        y = screen_geometry.center().y() - event.window.get_geometry().height / 2
                        event.window.configure(x=int(x), y=int(y), border_width=0, stack_mode=Above)  # Place the window where we want it.
                        event.window.map()  # Draw the window on the screen.
                        event.window.set_input_focus(RevertToParent, CurrentTime)  # Focus window
                    else:
                        print("Got an unknown event!")
                        print(event)
        except ConnectionClosedError as error:
            print("Connection closed:", error)
        except KeyboardInterrupt as error:
            print("Closing due to keyboard interrupt")
