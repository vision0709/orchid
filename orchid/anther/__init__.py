from os import environ
from Xlib.display import Display
from Xlib.X import SubstructureRedirectMask


class WindowManager:

    def __init__(self):
        display_num = environ.get("DISPLAY")
        if not display_num:
            display_num = ":0"

        print("Using display", display_num)
        self._display = Display(display_num)
        self._screens = []  # A list of all screens.
        self._screens.append(self._display.screen())  # Screen 0 is always the default screen.

        # Get references to all other screens.
        default_screen_num = self._display.get_default_screen()
        for i in range(0, self._display.screen_count()):
            if i != default_screen_num:
                self._screens.append(self._display.screen(i))

        self._screens[0].root.change_attributes(event_mask=SubstructureRedirectMask)  # Take control of window management.

        print("Control of root window gained")
        while True:
            if self._display.pending_events() > 0:  # If there is an event in the queue
                event = self._display.next_event()  # Grab it
                print("Got an event! ({})".format(str(event.type)))
