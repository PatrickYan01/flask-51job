#-*- coding = utf-8 -*-
#@Time : 2020/5/23 16:03
#@Author : Patrick
#@File : testcom.py
#@Software: PyCharm

import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.error,urllib.parse
import re
# import scrapy

def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('gbk', 'ignore')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

url = "https://jobs.51job.com/all/co2758227.html"
html = askURL(url)
bs = BeautifulSoup(html, "html.parser")
# 公司信息
CP_TYPE = ['民营公司', '上市公司', '事业单位', '国企', '外资（欧美）', '外资（非欧美）',
           '创业公司', '政府机关', '合资', '外资', '合资', '外企代表处', '非营利组织']
CP_SCALE = ['少于50人', '50-150人', '150-500人', '500-1000人',
            '1000-5000人', '5000-10000人', '10000人以上']


cp_info = bs.select('.in > p.ltype')[0].text.split('\xa0\xa0|\xa0\xa0')
com_data = {}
com_data['cp_type'] = com_data['cp_scale'] = com_data['industry'] = ''
for i in CP_TYPE:
    if i in cp_info:
        com_data['cp_type'] = i
        break
for i in CP_SCALE:
    if i in cp_info:
        com_data['cp_scale'] = i
        break
for i in cp_info:
    if i not in CP_TYPE and i not in CP_SCALE:
        com_data['industry'] = i

print(com_data)

