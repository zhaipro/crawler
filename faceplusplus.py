# coding: utf-8
# https://console.faceplusplus.com.cn/documents/4888373
import base64
import os
import sys

import requests

import settings


URL = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
ATTRIBUTES = [
    'gender',
    'age',
    'smiling',  # 注：对应在返回值的attributes中参数名为smile。在使用时请注意。
    'headpose',
    'facequality',
    'blur',
    'eyestatus',
    'emotion',
    'ethnicity',
    'beauty',
    'mouthstatus',
    'eyegaze',
    'skinstatus',
]
DATA = {
    'api_key': settings.KEY,
    'api_secret': settings.SECRET,
    'image_base64': 'UNKNOWN',                  # 请求时在填写
    'return_landmark': 2,                       # 检测。返回 106 个人脸关键点。
    'return_attributes': ','.join(ATTRIBUTES),  # 所有属性我们都要
}


def imread(fn):
    fp = open(fn, 'rb')
    return base64.b64encode(fp.read()).decode()


def detect(fn):
    DATA['image_base64'] = imread(fn)
    return requests.post(URL, data=DATA)


if __name__ == '__main__':
    path = './imgs_v2'
    for fn in os.listdir(path):
        _fn = os.path.join(path, fn)
        r = detect(_fn)
        print(fn, r.text, sep='\t')
        sys.stdout.flush()
