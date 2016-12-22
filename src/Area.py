import numpy as np
import cv2
from math import floor


class Area:
    def __init__(self, mark: int):
        self.min = [-1, -1]
        self.max = [0, 0]
        self.square = 0  # площадь
        self.mark = mark
        self.p_grid_size = 10
        self.p_grid = np.full((self.p_grid_size, self.p_grid_size), True, dtype=bool)
        self.contour = np.array((1, 1))
        self.region = np.array((1, 1))

    def add_point(self, point):
        self.square += 1
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

    def calc_contour(self, segmap: np.ndarray, src: np.ndarray):
        region = np.array(segmap[self.min[0]:self.max[0] + 1, self.min[1]:self.max[1] + 1], dtype=np.int32)
        if self.mark == 0:
            return

        region[region != self.mark] = 0
        self.region = np.array(region)
        _, contours, _ = cv2.findContours(region, 2, 1)
        if len(contours) > 1:
            region[region == self.mark] = 255
            max_ind = max(enumerate([len(cont) for cont in contours]), key=lambda x: x[1])
            self.contour = contours[max_ind[0]]
        else:
            print("no contour")

    def calc_contour_d(self, segmap: np.ndarray, src: np.ndarray):
        region = np.array(segmap[self.min[0]:self.max[0] + 1, self.min[1]:self.max[1] + 1], dtype=np.int32)
        if self.mark == 0:
            return

        region[region != self.mark] = 0
        self.region = np.array(region)
        _, contours, _ = cv2.findContours(region, 2, 1)
        if len(contours) > 1:
            region[region == self.mark] = 255
            max_ind = max(enumerate([len(cont) for cont in contours]), key=lambda x: x[1])
            imcopy = np.array(src[self.min[0]:self.max[0] + 1, self.min[1]:self.max[1] + 1])
            region = region.astype(np.uint8)
            for i in range(len(contours)):
                if i == max_ind[0]:
                    cv2.drawContours(region, contours, i, 200)
                    cv2.drawContours(imcopy, contours, i, (0, 0, 255))
                    print("contour (main): ", len(contours[i]))
                else:
                    cv2.drawContours(region, contours, i, 100)
                    cv2.drawContours(imcopy, contours, i, (0, 128, 128))
                    print("contour: ", len(contours[i]))
            print("total", len(contours), "contours")
            view2(imcopy, region)
            self.contour = contours[max_ind[0]]
        else:
            print("no contour")


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


def view(img, resize=False):
    cv2.namedWindow("view", cv2.WINDOW_NORMAL)
    if resize:
        cv2.resizeWindow("view", 1800, 1000)
    cv2.imshow("view", img)
    cv2.waitKey(0)
    cv2.destroyWindow("view")


# view without destroyWindow
def viewc(img, resize=False):
    winname = "view " + str(viewc.count)
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    minsize = 180
    if img.shape[0] < minsize or img.shape[1] < minsize:
        cv2.resizeWindow(winname, minsize, minsize)
    if resize:
        cv2.resizeWindow(winname, 1800, 1000)
    cv2.imshow(winname, img)
    viewc.count += 1


viewc.count = 1


def view2(img1, img2, resize=False):
    cv2.namedWindow("view1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("view2", cv2.WINDOW_NORMAL)
    if resize:
        cv2.resizeWindow("view1", 1800, 1000)
        cv2.resizeWindow("view2", 1800, 1000)
    cv2.imshow("view1", img1)
    cv2.imshow("view2", img2)
    cv2.waitKey(0)
    cv2.destroyWindow("view1")
    cv2.destroyWindow("view2")
