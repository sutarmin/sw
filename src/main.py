import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
from ImageRepository import ImageRepository as Repo

from utils import process, view
from history import effort1
from handlers import quantize, normalize_hist


def effort_cur(img):
    img = quantize(img, 5)
    img = normalize_hist(img)


if __name__ == '__main__':
    first, second = Repo.get_set(0)

    # занимаюсь выделением цветового канала из изображения

    print(first.shape)


    cv2.destroyAllWindows()
