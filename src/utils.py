import cv2
import numpy as np
from matplotlib import pyplot as plt
from ImageRepository import ImageRepository as Repo
from skimage.segmentation import quickshift
from Area import Area


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


def process_yield(img, func_arr):
    for obj in func_arr:
        if callable(obj):
            img = obj(img)
        else:
            for child in process_yield(img, obj):
                img = child
        yield img


def process(img, func_arr):
    result = None
    for result in process_yield(img, func_arr):
        pass
    return result


# показывает картинку с гистограммой полученного изображения
def show_hist_ex(img: np.ndarray):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        # plt.subplot(111)
        plt.plot(histr, color=col)
        plt.xlim([0, 256])

    plt.show()


def generate_dumps():
    for i in range(3):
        print('Set ' + str(i))
        left, right = Repo.get_set(i)
        seg = quickshift(left, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'graph/' + str(i) + '_left')
        seg = quickshift(right, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'graph/' + str(i) + '_right')


def generate_areas(seg_map: np.ndarray):
    areas = {}
    for i in range(seg_map.shape[0]):
        for j in range(seg_map.shape[1]):
            mark = seg_map.item((i, j))
            if mark not in areas.keys():
                areas[mark] = Area(mark)
            areas[mark].add_point([i, j])

    arr = list(areas.keys())
    for idx in arr:
        if areas[idx].square < 20:
            areas.pop(idx)
    return areas


def write_area_to_file(arr: np.ndarray, _min=None, _max=None, filename='temp.txt'):
    if _min is None:
        _min = (0, 0)
    if _max is None:
        _max = arr.shape
    with open(filename, 'w') as f:
        for i in range(_min[0], _max[0]):
            for j in range(_min[1], _max[1]):
                f.write("{: >3}".format(arr.item((i, j))))
            f.write('\n')


def draw_contour_on_region(region: np.ndarray, contour, value, shift=(0, 0)):
    for point in contour:
        x = point[0][0] + shift[1]
        y = point[0][1] + shift[0]
        if len(region.shape) == 3:
            region.itemset((y, x, 0), value[0])
            region.itemset((y, x, 1), value[1])
            region.itemset((y, x, 2), value[2])
        else:
            region.itemset((y, x), value)
