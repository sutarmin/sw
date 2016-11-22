import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import exposure


# эквализация гисторграммы (повышение контрастности) цветного изображения с помощью CLAHE
def get_clahe_from_rgb_image(src: np.ndarray):
    clahe_filter = cv2.createCLAHE()
    src_b = src[:, :, 0]
    src_g = src[:, :, 1]
    src_r = src[:, :, 2]
    clahe_src_r = clahe_filter.apply(src_r)
    clahe_src_g = clahe_filter.apply(src_g)
    clahe_src_b = clahe_filter.apply(src_b)
    res = np.stack((clahe_src_b, clahe_src_g, clahe_src_r), axis=2)
    return res


# дискретизация изображения
def quantize(src: np.ndarray, colors_per_channel: int):
    times = 256 / colors_per_channel
    res = src.copy()
    shape = src.shape
    width = shape[0]
    height = shape[1]
    for chanel in range(shape[2]):
        for w in range(width):
            for h in range(height):
                val = res.item((w, h, chanel))
                res.itemset((w, h, chanel), (val // times) * times)
    return res


# собственная реализвация нормализации гисторграммы
def normalize_hist_own(img: np.ndarray):
    def is_enough_weight(x: int):
        if x < 10:
            return False
        return True

    res = img.copy()
    color = ('b', 'g', 'r')
    for ind, col in enumerate(color):
        hist = cv2.calcHist([img], [ind], None, [256], [0, 256])
        minInd = 0
        while not is_enough_weight(hist[minInd]):
            minInd += 1
        maxInd = 255
        while not is_enough_weight(hist[minInd]):
            maxInd -= 1

        def func(x: int):
            return (x - minInd) * 255 / (maxInd - minInd)

        for x in range(res.shape[0]):
            for y in range(res.shape[1]):
                item = res.item((x, y, ind))
                res.itemset((x, y, ind), func(item))
    return res


def normalize_hist(img: np.ndarray):
    p2, p98 = np.percentile(img, (2, 98))
    res = exposure.rescale_intensity(img, in_range=(p2, p98))
    return res


# показывает картинку с гистограммой полученного изображения
def show_hist_ex(img: np.ndarray):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        # plt.subplot(111)
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()

