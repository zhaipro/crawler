# coding:utf-8
import sys

import cv2


# 定义分类器（正脸识别）
HAAR_ALT = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
LBP_IMPROVED = cv2.CascadeClassifier('./data/lbpcascade_frontalface_improved.xml')


def dbg(s):
    print(s)
    sys.stdout.flush()


def detect_multi_face(im, classifier=HAAR_ALT):
    if isinstance(im, str):
        im = cv2.imread(im)
    assert im is not None
    # 这些参数的效果是？
    faces = classifier.detectMultiScale(im, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, (50, 50))
    return faces


if __name__ == "__main__":
    r = detect_multi_face('a.jpg')
    dbg(r)
