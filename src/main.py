import numpy as np
import cv2
from skimage.segmentation import quickshift, felzenszwalb, mark_boundaries

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import ImageBuilder
from Comparer import Comparer
from utils import viewc

if __name__ == '__main__':
    src1 = cv2.imread('../img/synthetic/arrows_1.png')
    src2 = cv2.imread('../img/synthetic/arrows_2.png')
    src1, src2 = Repo.get_set(0)
    comparer = Comparer(0.02, 1.5)
    comparer.add(src1)
    comparer.add(src2)
    print(comparer.compare_dict)
    res1, res2 = comparer.draw_diff(0, 1)
    viewc(res1)
    viewc(res2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
