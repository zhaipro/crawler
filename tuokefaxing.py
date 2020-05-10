# coding: utf-8
# 脱壳发型
import hashlib
import json
import os
import pathlib

import requests


PATH = 'tuokefaxing'
pathlib.Path(PATH).mkdir(exist_ok=True)


def get(path, **kws):
    url = f'https://api.tuokefaxing.com{path}'
    headers = {
        'appid': 'tk1706852019512',
        'noncestr': 'd55210c0-53fe-43fa-ac17-8dfbd830e008',
        'sign': '350e7a168dedccf6c9b58dc9ac50111716d58088',
        # 'Authorization': 'Token qtVlmDiN3f0IHhBSOsWo7mJo0oH1xeYHJsWpyfdfSJoKn4fBwOHjIFuSCPp1dWAc2a4mBV',
    }
    r = requests.get(url, headers=headers, params=kws)
    return r.text


# get('/api/sys/tags')
# get('/api/chatroom/hot')
# get('/api/topic/week/recommends')
# get('/api/sys/aggregate/pager', page=1, pagesize=12)


def get_album_cate_top():
    with open('album_cate_top.txt', 'w', encoding='utf-8') as fp:
        text = get('/api/album/cate/top')
        fp.write(text)


def get_album_cate():
    fp = open('album_cate_top.txt', encoding='utf-8')
    result = json.load(fp)
    with open('album_cate.txt', 'w', encoding='utf-8') as fp:
        for data in result:
            id = data['id']
            url = f'/api/album/cate/{id}'
            text =  get(url)
            fp.write(f'{id}\t{text}\n')


def get_chatroom_category():
    with open('chatroom_category.txt', 'w', encoding='utf-8') as fp:
        for line in open('album_cate.txt', encoding='utf-8'):
            _, text = line.split('\t')
            text = json.loads(text)
            for result in text:
                for child in result['children']:
                    id = child['id']
                    url = f'/api/chatroom/category/{id}'
                    text = get(url)
                    fp.write(f'{id}\t{text}\n')


# get_chatroom_category()


def get_album_cate_files():
    with open('album_cate_files.txt', 'w', encoding='utf-8') as fp:
        for line in open('album_cate.txt', encoding='utf-8'):
            _, text = line.split('\t')
            text = json.loads(text)
            for result in text:
                for child in result['children']:
                    id = child['id']
                    url = f'/api/album/cate/{id}/files'
                    text = get(url, page=1, pagesize=30)
                    r = json.loads(text)
                    for i in range(r['totalpage']):
                        text = get(url, page=1 + i, pagesize=30)
                        fp.write(f'{id}\t{i}\t{text}\n')


def get_album_file():
    with open('album_file.txt', 'w', encoding='utf-8') as fp:
        for line in open('album_cate_files.txt', encoding='utf-8'):
            _, _, text = line.split('\t')
            text = json.loads(text)
            for item in text['items']:
                id = item["id"]
                url = f'/api/album/file/{id}'
                text = get(url)
                fp.write(f'{id}\t{text}\n')


def imdonwload(fn, url):
    fn = params['id']
    fn = f'{PATH}/{fn}.png'
    if os.path.isfile(fn):
        print('downloaded:', fn)
        return
    print('downloading:', fn)
    try:
        r = requests.get(url, timeout=15)
        im = r.content
        with open(fn, 'wb') as fp:
            fp.write(im)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass


def main():
    fp = open('album_file.txt', encoding='utf-8')
    lines = fp.readlines()
    for line in lines:
        _, text = line.split('\t')
        text = json.loads(text)
        id = text['id']
        url = text['fileviewurl']
        imdonwload(id, url)


def download_album_files():
    for line in open('album_cate_files.txt', encoding='utf-8'):
        _, _, text = line.split('\t')
        text = json.loads(text)
        for item in text['items']:
            id = item["id"]
            url = item['fileurl'][:-6]
            imdonwload(id, url)


# get_album_cate_top()
# get_album_cate()
# get_album_cate_files()
# get_album_file()
# main()
download_album_files()
