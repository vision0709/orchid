from os import environ
from Xlib.display import Display
from Xlib.X import SubstructureRedirectMask, MapRequest, KeyPress, RevertToParent, CurrentTime, Above
from Xlib.error import ConnectionClosedError
from orchid.anther.utils.Geometry import Bounds


class WindowManager:

    def __init__(self):
        #display_num = environ.get("DISPLAY")
        #if not display_num:
        display_num = ":1"  # TODO: Don't force this to be 1.

        self._display = Display(display_num)  # Create the connection to the X server.
        self._default_screen = self._display.screen()  # Get the default screen.
        self._default_screen.root.change_attributes(event_mask=SubstructureRedirectMask)  # Take control of window management on the default screen.
        # TODO: Manage more than just the default screen.

        print("Control of default root window gained")

        # Calculate window bounds on the screen.
        screen_width = self._default_screen.width_in_pixels
        screen_height = self._default_screen.height_in_pixels
        self._default_screen_bounds = Bounds(screen_width * .02, screen_width, screen_height * .1, screen_height)

        try:
            while True:
                if self._display.pending_events() > 0:  # Check if there are any pending events in the queue.
                    event = self._display.next_event()  # Get the next pending event.
                    if event.type == KeyPress:
                        print("Got a key press event!")
                    elif event.type == MapRequest:
                        print("Got a map request event!")
                        event.window.map()
                        event.window.set_input_focus(RevertToParent, CurrentTime)  # Focus window
                        x = self._default_screen_bounds.center.x - event.window.get_geometry().width / 2
                        y = self._default_screen_bounds.center.y - event.window.get_geometry().height / 2
                        print(int(x), " x ", int(y))
                        event.window.configure(x=int(x) - 1, y=int(y) - 1, border_width=2, stack_mode=Above)  # Place the window where we want it.
                    else:
                        print("Got an unknown event!")
        except ConnectionClosedError as error:
            print("Connection closed:", error)
