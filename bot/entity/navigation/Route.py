class Route:
    def __init__(self, weight, dst, path):
        self.weight = weight
        self.dst = dst
        self.path = path

    def __repr__(self):
        return f"Route(weight={self.weight}, dst={self.dst}, path={self.path})"

    def __lt__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight < other.weight

    def __le__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight <= other.weight


    def __gt__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight > other.weight


    def __ge__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight >= other.weight


    def __eq__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight == other.weight


    def __ne__(self, other):
        if not isinstance(other, Route):
            return NotImplemented
        return self.weight != other.weight