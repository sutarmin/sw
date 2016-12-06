import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color

from skimage.segmentation import quickshift
from skimage.segmentation import mark_boundaries

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import imagebuilder as ib

from utils import process, process_yield, view
from history import effort2
from handlers import quantize, normalize_hist, get_channel



def effort_cur(img):
    img = quantize(img, 5)
    img = normalize_hist(img)


if __name__ == '__main__':
    first, second = Repo.get_set(0)
    # first = cv2.cvtColor(first, cv2.COLOR_RGB2BGR)
    # second = cv2.cvtColor(second, cv2.COLOR_RGB2BGR)

    quickshift_segments1 = quickshift(first, kernel_size=3, max_dist=6, ratio=0.5)
    quickshift_segments2 = quickshift(first, ratio=0.5)

    mark1 = mark_boundaries(first, quickshift_segments1)
    mark2 = mark_boundaries(first, quickshift_segments2)

    view(mark2 - mark1)

    # func_arr = effort2('r')
    # for i, f in enumerate(process_yield(first, func_arr)):
    #     ib.draw(f, (2, len(func_arr)), (1, i + 1))
    # for i, f in enumerate(process_yield(second, func_arr)):
    #     ib.draw(f, (2, len(func_arr)), (2, i + 1))
    # ib.show()

    # img = process(first, effort2('b'))

    cv2.destroyAllWindows()
