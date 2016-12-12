from skimage.segmentation import quickshift

from ImageRepository import ImageRepository as Repo
from handlers import quantize, normalize_hist, get_channel


def effort_cur(img):
    img = quantize(img, 5)
    img = normalize_hist(img)


def temp_main():
    for i in range(3):
        print('Set ' + str(i))
        left, right = Repo.get_set(i)
        seg = quickshift(left, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'quickshift/' + str(i) + '_left')
        seg = quickshift(right, kernel_size=3, max_dist=6, ratio=0.5)
        Repo.dump(seg, 'quickshift/' + str(i) + '_right')

if ё__name__ == '__main__':
    temp_main()
