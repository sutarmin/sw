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
    return areas


def write_area_to_file(arr: np.ndarray, _min, _max, filename='temp.txt'):
    with open(filename, 'w') as f:
        for i in range(_min[0], _max[0] + 1):
            for j in range(_min[1], _max[1] + 1):
                f.write("{: >4}".format(arr.item((i, j))))
            f.write('\n')