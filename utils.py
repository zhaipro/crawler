# coding:utf-8
import sys

import cv2


# 定义分类器（正脸识别）
HAAR_ALT = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
# 还是下面这个好
LBP_IMPROVED = cv2.CascadeClassifier('./data/lbpcascade_frontalface_improved.xml')


def dbg(*args):
    print(*args)
    sys.stdout.flush()


def detect_multi_face(im, classifier=LBP_IMPROVED):
    if isinstance(im, str):
        im = cv2.imread(im)
    assert im is not None
    # 这些参数的效果是？
    faces = classifier.detectMultiScale(im, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, (50, 50))
    return faces


def imcut(im):
    _h, _w = 833, 600   # 默认的剪切尺寸比
    if isinstance(im, str):
        im = cv2.imread(im)
    h, w, _ = im.shape
    ratio = min(h / _h, w / _w)
    h, c = int(ratio * _h), int((w - ratio * _w) / 2)
    im = im[:h, c:w-c]  # 扔掉底部或两侧
    return im


def imshow(im, faces):
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('im', im)


if __name__ == '__main__':
    import os

    fn = 'w.jpg'
    r = detect_multi_face(fn)
    dbg(r)
    im = imcut(fn)
    dbg(im.shape)

    path = './imgs_v2'
    im = cv2.imread(fn)
    faces = detect_multi_face(im, LBP_IMPROVED)
    dbg(fn, faces)
    imshow(im, faces)
    cv2.waitKey()
