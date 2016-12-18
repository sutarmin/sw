import numpy as np
import cv2
from skimage.segmentation import quickshift, felzenszwalb, mark_boundaries

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import ImageBuilder
from Image import Image

from handlers import quantize, normalize_hist, get_channel
from utils import view
from Area import Area


if __name__ == '__main__':
    # src = cv2.imread('../img/synthetic/arrows.png')
    src = cv2.imread('../img/0_left.jpg')
    # view(src[0:1, 0:1])
    img = Image(src)
