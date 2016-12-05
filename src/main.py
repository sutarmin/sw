import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
from ImageRepository import ImageRepository as Repo

from utils import process, process_yield, view
from history import effort2
from handlers import quantize, normalize_hist, get_channel


def effort_cur(img):
    img = quantize(img, 5)
    img = normalize_hist(img)


if __name__ == '__main__':
    first, second = Repo.get_set(0)
    first = cv2.cvtColor(first, cv2.COLOR_RGB2BGR)
    second = cv2.cvtColor(second, cv2.COLOR_RGB2BGR)

    img = process(first, effort2('b'))

    cv2.destroyAllWindows()
