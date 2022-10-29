import math

class Position:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, target) -> float:
        dy = target.y - self.y
        dx = target.x - self.x
        return math.sqrt(math.pow(dy, 2) + math.pow(dx, 2))

    def degress(self, target) -> float:
        dy = target.y - self.y
        dx = target.x - self.x
        return math.degrees(math.atan2(dy, dx))