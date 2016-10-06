import random


class Segment:
    def __init__(self):
        self.points = set()  # set of Point
        self.__hash_ = random.uniform(0, 100000)

    def __str__(self):
        return str(int(self.__hash_))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__hash_)

    def __eq__(self, other):
        return self.__hash_ == other.__hash_

        # old version of comparing
        # for point in self.points:
        #    if point not in other.points:
        #        return False
        # return True

    def __ne__(self, other):
        return not(self == other)

    @property
    def size(self):
        return len(self.points)

    def print_points(self):
        return "Points ({0}): {1}" \
            .format(len(self.points), self.points)

    def add_point(self, point: tuple):
        """
        :param point: tuple with coordinates (x, y)
        :return: None
        """
        assert(type(point) == tuple)
        assert (len(point) == 2)
        self.points.add(point)
