#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2020/4/11 13:17
# @Author  :Coco
# @FileName: 花瓣网爬取-静态版.py

# @Software: PyCharm
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓ ┏┓
            ┏┛┻━┛┻━┓
            ┃   ☃  ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
               ┃     ┗━━┓
               ┃        ┣┓
               ┃　      ┏┛
               ┗┓┓━━┳┓━┛
                 ┃┫  ┃┫
                 ┗┛  ┗┛
"""
'''
静态爬取 花瓣网图片资源
改脚本只能爬取一页 
协程 并发 执行下载文件
'''
import requests
import gevent
import re
import os
import time
from gevent import monkey

monkey.patch_all()
URL = 'https://huaban.com/search/?q=%s&page=%d&per_page=20&wfl=1'
IMAGE = 'https://hbimg.huabanimg.com/'
KEY = 'coco'


def get_image_list():
    '''
    从元代马忠获取image 链接
    :param image_link_list:
    :return:
    '''
    result = []
    for i in range(1, 5):
        date = requests.get(URL + KEY)
        if date.status_code == 200:
            temp = date.content.decode('utf-8')
            image_key = re.findall('"key":"(.*?)"', temp.split('app.page["facets"]')[1], re.S)
            result += image_key
    return result


def down_load_image(image_key):
    '''
    下载image
    :param image_key:
    :return:
    '''
    image = requests.get(url=IMAGE + image_key).content
    if not os.path.exists('image/' + image_key + '.jpg'):
        with open('image/' + image_key + '.jpg', 'wb') as f:
            f.write(image)


if __name__ == '__main__':
    image_key_list = get_image_list()
    print(image_key_list)
    if not os.path.exists('image/'):
        os.mkdir('image')
    start = time.time()
    print('总文件数 %s 开始爬取：' % len(image_key_list))
    gevent.joinall([gevent.spawn(down_load_image, i) for i in image_key_list])
    end = time.time()
    print('Cost time：', end - start)
