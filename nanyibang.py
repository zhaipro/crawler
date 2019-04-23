# coding: utf-8
import pathlib
import sys

import requests


PATH = 'nanyibang'
pathlib.Path(PATH).mkdir(exist_ok=True)
KIND2CATES = {
    1: [8, 10, 12, 14],
    2: [16, 18, 20, 22, 24, 26, 28, 30, 38, 42],
    3: [32, 34, 36],
}
KINDS = {
    1: '短发',
    2: '中发',
    3: '长发',
}
CATES = {
    8: '侧分',
    10: '寸头',
    12: '碎发',
    14: '油发',

    16: '背头',
    18: '飞机头',
    20: '锅盖头',
    22: '刘海',
    24: '蓬巴杜',
    26: '西瓜头',
    28: '斜庞克',
    30: '中分',
    38: '侧分',
    42: '卷发',

    32: '丸子头',
    34: '卷发',
    36: '长发',
}


def dbg(s):
    print(s)
    sys.stdout.flush()


def download(kind, cate):
    url = 'https://xcx.nanyibang.com/hair'
    last_page = 1
    i = 1
    while i <= last_page:
        params = {
            'page': i,
            'kindId': kind,    # [1, 2, 3]
            'cateId': cate,
        }
        r = requests.get(url, params=params)
        data = r.json()['data']
        last_page = data['last_page']
        for data in data['data']:
            hair_id = data['hair_id']
            title = data['title']
            picture = data['picture']
            r = requests.get(picture, timeout=13)
            dbg(picture)
            with open(f'{PATH}/{KINDS[kind]}.{CATES[cate]}.{title}.{hair_id}.jpg', 'wb') as fp:
                fp.write(r.content)
        i += 1


if __name__ == '__main__':
    for kind, cates in KIND2CATES.items():
        for cate in cates:
            download(kind, cate)
