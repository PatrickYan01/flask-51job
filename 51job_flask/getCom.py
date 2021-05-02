#-*- coding = utf-8 -*-
#@Time : 2020/5/22 15:46
#@Author : Patrick
#@File : testArea.py
#@Software: PyCharm

import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.error,urllib.parse
import re

findLink = re.compile(r'<p class="t1">.*<a.*href="(.*?)"', re.S)
findArea = re.compile('<span class="t3">(.*)</span>\n<span class="t4">', re.S)
findComLink = re.compile(r'<span class="t2"><a.*href="(.*?)"', re.S)
findCom = re.compile(r'<span class="t2"><a.*title="(.*?)"', re.S)


def main():
    kw = input("请输入你要搜索的岗位关键字：").strip()
    keyword = urllib.parse.quote(urllib.parse.quote(kw))   #二次编码
    # ka = input("请输入你要搜索的地区：").strip()
    # karea = getArea(ka)

    for i in range(1, 165):
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

            com = re.findall(findCom, item)
            data['com'] = ''.join(com)

            comlink = re.findall(findComLink, item)
            data['comlink'] = ''.join(comlink)

            strhtml = 'https://jobs.51job.com/'
            if data["link"].startswith(strhtml):
                # datalist.append(data)
                # print(data['comlink'])
                com_link = data['comlink']
                com_data = getCOM(com_link)
                data = dict(data.items(), **com_data)
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


def getCOM(com_link):
    com_html = askURL(com_link)
    bs = BeautifulSoup(com_html, "html.parser")
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

    return com_data


def saveDB(datalist, dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        print(data)
        sql = '''
                insert or ignore into job_com(
                link,area,company,comlink,cp_type,cp_scale,cp_industry
                 ) 
                 values(?,?,?,?,?,?,?)'''
        # print(sql)
        cur.execute(sql, (data['link'], data['area'], data['com'], data['comlink'], data['cp_type'], data['cp_scale'], data['industry']))
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
            create table job_com
            (
            
            area text,
            company text,
            comlink text,
            cp_type text,
            cp_scale text,
            cp_industry text,
            link text FOREIGN KEY REFERENCES job_quanguo(link)
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

