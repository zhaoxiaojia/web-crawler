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

import requests
import gevent
from gevent import monkey
import re
import os
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# monkey.patch_all()

URL = 'https://huaban.com/search/?q='
IMAGE = 'https://hbimg.huabanimg.com/'
KEY = 'coco'

cookie_str = r'BAIDU_SSP_lcr=https://www.baidu.com/link?url=3rEXMvdDa4y71K-9XAU-pqKwLZIn9A0rIvebYPOzmdC&wd=&eqid=9b458abb000c715f000000045e918821; _uab_collina=158657970359405935620147; UM_distinctid=171678507a43f5-0a23b6d55059e8-2393f61-1fa400-171678507a5ae2; __auc=a8541a2717167850a27ac1bda3a; __gads=ID=022a6394fc6a1710:T=1586579729:S=ALNI_MawYgqGeaLxoqXGQlE8KyQNqE-vNw; __asc=42a79a9317167b56ed58c218027; _ga=GA1.2.1175684574.1586592467; _gid=GA1.2.1989343252.1586592467; CNZZDATA1256903590=1759746214-1586576051-https%253A%252F%252Fwww.baidu.com%252F%7C1586593254; referer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D3m43efL7UwOAIYnmHvDvkG0uOnrzr9YygCatlhoFzlm%26wd%3D%26eqid%3D98f66177000a6da6000000045e91855e; uid=29615027; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAACuUlEQVRYR%2B2WT0gUURzHP287FCpKhyQINZIOmUGQk0jBjBERGd3yICQFSXQITYKsQwcvegjapVvboQw8FBFEWUS1sxCIrh2CtCCMTAjJCoJYpNAXv9lZWNfdcdRZSWhOD9533vt%2Bfv9mFFprvB6llOf%2BKm2Gf4Q9fSoBKUomiba1OZbaIxEi7e3Oui0aJVlc7AmioQiIAjcUxAvF5QtELjfjKQ9x05y3xkdGNOwAhHjknwPZMDNDa18fLf39FjAK3AYuABNuBlqAfkkcUAU0AFeAKeAokMyhk%2F1S4Ehap%2BCbH%2FglZcS2xHPqsWybr%2BXljNXUGBJpDceBt0C57EsZ6ZShYWATcM4FNTKNeeia5DwF7wIHyS6tPCDTwCOgHhhyoy8gTmm5ZVYLxPLoahXcSwdmNUGa3YsvAw8AMSmZkRKTUrnqZiRt0HQjLJnz0jkZDhQkc2pd6unhbnMz49XVdPX28rmyUqIu0X8KvAGeALYLMgCUAd3AKeBiRt9IiWXrpH%2F2ASeBW7KvoCvQ0sp7mI%2Bp5cfISjW%2Bm%2F0%2FyEpD7fP9gmREx4cOoFWf40HpVvS66zBXJmtl1r%2FM9qbtkVHQNaDGlFW3M593L102iPllGx9LvzNZ8jNlY7n%2FWtoe7ga1W1nGMW0nzjuHWca1hRCOrklZxh5tJ16DfqysvTLt5j3ueXl1aZCKX2UcmtzuvPus4kMQIIkTKM4o09ivYyNhQrMPc2YjnnjOHJ9Uo3FaxxI3CbFVmcbBBSCL6DIzIjANU1UMbp5YOYgY0fHEKzT30apKNdZ15CoZvSZAJMLK%2Bc8ayFVWLuwayEiqT84Cncoy7uTMSEoTWI%2FIHQUoLZleoQ5peK8pmj2NnF5R%2BnD2lPPSRXYNvkhDSLOX%2FFnP79AssS3jvN84vfyp5XP8ByYryHckMHdLOGgxkL8g0%2BMoiUoFIQAAAABJRU5ErkJggg%3D%3D%2CWin32.1920.1080.24; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1586579991,1586592762,1586595171,1586595876; sid=s%3AsPssXyidFhfcg_ATVz7VyNqKxq--r1q-.PtLVzXkEKmlLHHDUi5W68%2BuN5a4dn76qg%2FeX4MZ2MiY; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1586596751909; Hm_lpvt_d4a0e7c3cd16eb58a65472f40e7ee543=1586596751'
cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def get_more_iamge():
    '''
    获取滚动之后的网页源代码
    :return:
    '''
    browser = webdriver.Chrome()
    browser.get(URL + KEY, )
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'wrapper')))
    soup = BeautifulSoup(browser.page_source, 'lxml')
    js = "var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    time.sleep(5)
    browser.close()
    print(soup)


def get_image_list():
    '''
    从元代马忠获取image 链接
    :param image_link_list:
    :return:
    '''
    date = requests.get(URL + KEY).content.decode('utf-8')
    # print(date)
    image_key = re.findall('"key":"(.*?)"', date.split('app.page["facets"]')[1], re.S)
    return list(set(image_key))


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
    # image_link_list = get_more_iamge()
    image_key_list = get_image_list()
    if not os.path.exists('image/'):
        os.mkdir('image')
    start = time.time()
    print('总文件数 %s 开始爬取：' % len(image_key_list))
    gevent.joinall([gevent.spawn(down_load_image, i) for i in image_key_list])
    end = time.time()
    print('Cost time：', end - start)
