# coding: utf-8
import pathlib
import base64
import re

import requests


PATH = __file__[:-3]
pathlib.Path(PATH).mkdir(exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0'}


def gen_fn(url):
    fn = re.search(r'p?\d+.jpe?g', url)
    return fn.group()


for url in open('bobo.txt'):
    url = url.strip()
    r = requests.get(url, headers=headers)
    fn = gen_fn(url)
    with open(f'{PATH}/{fn}', 'wb') as fp:
        fp.write(r.content)
    if fn[0] == 'p':
        url = url[:-len(fn)] + fn[1:]
        fn = gen_fn(url)
        r = requests.get(url, headers=headers)
        with open(f'{PATH}/{fn}.jpg', 'wb') as fp:
            fp.write(r.content)
