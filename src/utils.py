import cv2


def view(img):
    cv2.namedWindow("view", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("view", 1800, 1000)
    cv2.imshow("view", img)
    cv2.waitKey(0)
    cv2.destroyWindow("view")


def process_yield(img, func_arr):
    for obj in func_arr:
        if callable(obj):
            img = obj(img)
        else:
            for child in process_yield(img, obj):
                img = child
        yield img



def process(img, func_arr):
    result = None
    for result in process_yield(img, func_arr):
        pass
    return result
