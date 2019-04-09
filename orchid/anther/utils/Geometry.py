class Point:
    """
    A 2-dimensional point in space for positioning windows.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        A 2-dimensional point in space.

        :param x: The x-coordinate in space.
        :type x: int
        :param y: The y-coordinate in space.
        :type y: int
        """
        self.x = x
        self.y = y


class Bounds:
    """
    A bounding box for positioning windows.
    """

    def __init__(self, left: float = 0, right: float = 0, top: float = 0, bottom: float = 0) -> None:
        """
        A bounding box for positioning windows.

        :param left: The leftmost value inside the box.
        :type left: float
        :param right: The rightmost value inside the box.
        :type right: float
        :param top: The topmost value inside the box.
        :type top: float
        :param bottom: The bottommost value inside the box.
        :type bottom: float
        """
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.center = Point(self.width / 2, self.height / 2)
