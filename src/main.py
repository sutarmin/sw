import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.segmentation import quickshift, felzenszwalb, mark_boundaries, slic
from skimage.util import img_as_float

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import ImageBuilder
from Comparer import Comparer
from utils import viewc
from handlers import normalize_hist
from time import time


def main():
    src1 = cv2.imread('../img/synthetic/arrows_1.png')
    src2 = cv2.imread('../img/synthetic/arrows_2.png')
    # src1, src2 = Repo.get_set(0)
    comparer = Comparer(0.02, 0)
    comparer.add(src1)
    comparer.add(src2)
    print(comparer.compare_dict)
    res1, res2 = comparer.draw_diff(0, 1)
    viewc(res1)
    viewc(res2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    """
    first, second = Repo.get_set(0)
    img = cv2.cvtColor(first, cv2.COLOR_RGB2BGR)

    start = time()
    segments_fz = felzenszwalb(img, scale=100, sigma=1.1, min_size=50)
    print("felzenszwalb", time() - start)
    print("number of segments: %d" % len(np.unique(segments_fz)))
    start = time()
    segments_slic = slic(img, n_segments=1000, compactness=10, sigma=1)
    print("slic", time() - start)
    print("number of segments: %d" % len(np.unique(segments_slic)))
    start = time()
    segments_quick = quickshift(img, kernel_size=1, max_dist=15, ratio=0.7)
    print("quickshift", time() - start)
    print("number of segments: %d" % len(np.unique(segments_quick)))

    fig, ax = plt.subplots(2, 2, sharex=True, sharey=True, subplot_kw={'adjustable': 'box-forced'})
    fig.set_size_inches(8, 3, forward=True)
    fig.subplots_adjust(0.05, 0.05, 0.95, 0.95, 0.05, 0.05)
    ax[0][0].imshow(img)
    ax[0][1].imshow(mark_boundaries(img, segments_fz))
    ax[1][0].imshow(mark_boundaries(img, segments_slic))
    ax[1][1].imshow(mark_boundaries(img, segments_quick))
    ax[0][0].set_title("Original image")
    ax[0][1].set_title("Felzenszwalbs's method")
    ax[1][0].set_title("SLIC")
    ax[1][1].set_title("Quickshift")

    plt.show()
"""