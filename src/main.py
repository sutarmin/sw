import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import skimage
from skimage import exposure, morphology, color
import time
import pickle
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


def temp_not_main():
    first, second = Repo.get_set(0)
    first = cv2.cvtColor(first, cv2.COLOR_RGB2BGR)
    # second = cv2.cvtColor(second, cv2.COLOR_RGB2BGR)



    start = time.process_time()
    print("start")
    quickshift_segments1 = quickshift(first, kernel_size=3, max_dist=6, ratio=0.5)
    # quickshift_segments2 = quickshift(first, ratio=0.5)
    print("done. caching")
    with open('../img/dumps/quickshift/0_left.pkl', 'wb') as f:
        pickle.dump(quickshift_segments1, f)

    print(time.process_time() - start)

    mark1 = mark_boundaries(first, quickshift_segments1)

    cv2.destroyAllWindows()


def temp_main():
    first, second = Repo.get_set(0)
    print("Start")
    quickshift_seg = quickshift(second, kernel_size=3, max_dist=6, ratio=0.5)
    print("Done")
    Repo.dump(quickshift_seg, 'quickshift/0_right')


if __name__ == '__main__':
    temp_main()
