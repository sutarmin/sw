import numpy as np
import cv2
from math import floor


class Area:
    def __init__(self, mark: int):
        self.min = [-1, -1]
        self.max = [0, 0]
        self.mark = mark
        self.p_grid_size = 10
        self.p_grid = np.full((self.p_grid_size, self.p_grid_size), True, dtype=bool)
        self.contour = np.array((1, 1))
        self.region = np.array((1, 1))

    def add_point(self, point):
        if self.min[0] > point[0] or self.min[0] == -1:
            self.min[0] = point[0]
        if self.min[1] > point[1] or self.min[1] == -1:
            self.min[1] = point[1]
        if self.max[0] < point[0]:
            self.max[0] = point[0]
        if self.max[1] < point[1]:
            self.max[1] = point[1]

    def calc_p_grid(self, segmap: np.ndarray):

        step_h = (self.max[0] - self.min[0]) / self.p_grid_size
        step_w = (self.max[1] - self.min[1]) / self.p_grid_size

        for i in range(self.p_grid_size):
            from_h = floor(i * step_h) + self.min[0]
            to_h = floor((i + 1) * step_h) + self.min[0]
            for j in range(self.p_grid_size):
                from_w = floor(j * step_w) + self.min[1]
                to_w = floor((j + 1) * step_w) + self.min[1]
                # print('[{0}:{1}][{2}:{3}]'.format(from_h, to_h, from_w, to_w))
                if not np.any(segmap[from_h:to_h + 1, from_w:to_w + 1] == self.mark):
                    self.p_grid.itemset((i, j), False)

    def calc_contour(self, segmap: np.ndarray):
        region = np.array(segmap[self.min[0]:self.max[0] + 1, self.min[1]:self.max[1] + 1], dtype=np.int32)
        if self.mark == 0:
            return

        region[region != self.mark] = 0
        self.region = np.array(region)
        _, contour, _ = cv2.findContours(region, 2, 1)
        if len(contour) > 1:
            self.contour = contour[0]


def write_area_to_file(arr: np.ndarray, _min=None, _max=None, filename='temp.txt'):
    if _min is None:
        _min = (0, 0)
    if _max is None:
        _max = arr.shape
    with open(filename, 'w') as f:
        for i in range(_min[0], _max[0]):
            for j in range(_min[1], _max[1]):
                f.write("{: >2}".format(arr.item((i, j))))
            f.write('\n')