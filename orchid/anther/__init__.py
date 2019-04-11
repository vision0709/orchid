from PyQt5.QtCore import QObject
from os import environ
from Xlib.display import Display
from Xlib.X import SubstructureRedirectMask, MapRequest, KeyPress, RevertToParent, CurrentTime, Above
from Xlib.error import ConnectionClosedError, BadAccess
from orchid.utils.Geometry import Bounds


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
        print("Using display", display_num)
        if not display_num:
            display_num = ":0"

        self._display = Display(display_num)  # Create the connection to the X server.
        self._default_screen = self._display.screen()  # Get the default screen.

        # Take control of window management on the default screen.
        try:
            # TODO: Manage more than just the default screen.
            self._default_screen.root.change_attributes(event_mask=SubstructureRedirectMask)
            print("Control of default root window gained")
        except BadAccess as error:
            print("Error")

        # Calculate window bounds on the screen.
        screen_width = self._default_screen.width_in_pixels
        screen_height = self._default_screen.height_in_pixels
        self._default_screen_bounds = Bounds(screen_width * .02, screen_width, screen_height * .1, screen_height)

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
        The main loop of the Window Manager.
        """
        try:
            while self.is_running:
                if self._display.pending_events() > 0:  # Check if there are any pending events in the queue.
                    event = self._display.next_event()  # Get the next pending event.
                    if event.type == KeyPress:
                        print("Got a key press event!")
                    elif event.type == MapRequest:
                        print("Got a map request event!")
                        x = self._default_screen_bounds.center.x - event.window.get_geometry().width / 2
                        y = self._default_screen_bounds.center.y - event.window.get_geometry().height / 2
                        print(int(x), " x ", int(y))
                        event.window.configure(x=int(x) - 1, y=int(y) - 1, border_width=2,
                                               stack_mode=Above)  # Place the window where we want it.

                        event.window.map()
                        event.window.set_input_focus(RevertToParent, CurrentTime)  # Focus window
                    else:
                        print("Got an unknown event!")
        except ConnectionClosedError as error:
            print("Connection closed:", error)
        except KeyboardInterrupt as error:
            print("Closing due to keyboard interrupt")

    def get_screen_width(self) -> float:
        """
        Returns the width of the screen in pixels.

        :return: The width of the screen in pixels.
        :rtype: float
        """
        return self._default_screen_bounds.right

    def get_screen_height(self) -> float:
        """
        Returns the height of the screen in pixels.

        :return: The height of the screen in pixels.
        :rtype: float
        """
        return self._default_screen_bounds.bottom
