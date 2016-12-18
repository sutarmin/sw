import numpy as np
from math import floor


class Area:
    def __init__(self, mark: int):
        self.min = [-1, -1]
        self.max = [0, 0]
        self.mark = mark
        self.p_grid_size = 10
        self.p_grid = np.full((self.p_grid_size, self.p_grid_size), True, dtype=bool)

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
