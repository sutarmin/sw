import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
from ImageRepository import ImageRepository as Repo

from utils import process, view
from history import effort1

if __name__ == '__main__':
    first, second = Repo.get_set(0)

    for img in process(second, effort1):
        view(img)

    cv2.destroyAllWindows()
