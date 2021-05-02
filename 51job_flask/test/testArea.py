#-*- coding = utf-8 -*-
#@Time : 2020/5/22 15:46
#@Author : Patrick
#@File : testArea.py
#@Software: PyCharm

import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.error,urllib.parse
import re

findLink = re.compile(r'<a.*href="(.*?)"', re.S)
findArea = re.compile('<span class="t3">(.*)</span>\n<span class="t4">', re.S)

def main():
    kw = input("请输入你要搜索的岗位关键字：").strip()
    keyword = urllib.parse.quote(urllib.parse.quote(kw))   #二次编码
    # ka = input("请输入你要搜索的地区：").strip()
    # karea = getArea(ka)

    for i in range(1, 2):
        print('正在爬取第{}页信息'.format(i))
        baseurl = "https://search.51job.com/list/"+ str(000000) +",000000,0000,00,9,99,"+ keyword +",2,"+ str(i) +".html"    #深圳+keyword
        html = askURL(baseurl)
        bs = BeautifulSoup(html,"html.parser")

        datalist = []
        for item in bs.find_all("div", {"class": "el"}):
            data = {}
            item = str(item)

            link = re.findall(findLink, item)
            data['link'] = ''.join(link)

            area = re.findall(findArea, item)
            data['area'] = ''.join(area)

            strhtml = 'https://jobs.51job.com/'
            if data["link"].startswith(strhtml):
                datalist.append(data)
        dbpath = "./51job.db"
        saveDB(datalist, dbpath)
        print(datalist)


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


def findData(bs):

    for item in bs.find_all("div", {"class": "el"}):

        item = str(item)

        link = re.findall(findLink, item)
        # data.append(link)

        area = re.findall(findArea, item)
        # data.append(area)

    datalist.append({"link":''.join(link),"area":''.join(area)})

    print(datalist)


def saveDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        print(data)
        sql = '''
                insert or ignore into job_area(
                link,area
                 ) 
                 values(?,?)'''
        # print(sql)
        cur.execute(sql, (data['link'], data['area']))
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
            create table job_area
            (
            link text PRIMARY KEY,
            area text
            )
        '''
    # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

    print('Table created successfully')

if __name__ == "__main__":
    main()

