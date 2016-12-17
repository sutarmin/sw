import numpy as np
from skimage.segmentation import quickshift

from ImageRepository import ImageRepository as Repo
from MultiImageViewer import ImageBuilder

from handlers import quantize, normalize_hist, get_channel


def generate_areas(seg_map: np.ndarray):
    # возвращать по одному объектику, если это возможно
    yield seg_map


def generate_dumps():
    for i in range(3):
        print('Set ' + str(i))
        left, right = Repo.get_set(i)
        seg = quickshift(left, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'quickshift/' + str(i) + '_left')
        seg = quickshift(right, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'quickshift/' + str(i) + '_right')


if __name__ == '__main__':
    left, right = Repo.get_set_from_dumpq(0)

    print(left)
