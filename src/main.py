import numpy as np
import cv2
from skimage.segmentation import quickshift, felzenszwalb, mark_boundaries

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import ImageBuilder
from Image import Image, compare

from handlers import quantize, normalize_hist, get_channel
from utils import view
from Area import Area

if __name__ == '__main__':
    src1 = cv2.imread('../img/synthetic/cloud1.png')
    src2 = cv2.imread('../img/synthetic/cloud2.png')
    # src = cv2.imread('../img/0_left.jpg')
    img1 = Image(src1)
    img2 = Image(src2)
    compare(img1, img2)
