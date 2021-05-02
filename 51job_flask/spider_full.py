#-*- coding = utf-8 -*-
#@Time : 2020/5/18 14:26
#@Author : Patrick
#@File : spider.py
#@Software: PyCharm


import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.error,urllib.parse
import re


jobList = []

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

        datalist = getData(bs)
        dbpath = "./51job.db"
        saveDB(datalist, dbpath)
    # print(datalist)


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


findLink = re.compile(r'<p class="t1">.*<a.*href="(.*?)".*</p>', re.S)  #匹配招聘岗位链接
findTitle = re.compile(r'<p class="t1">.*<a.*title="(.*)".*</p>',re.S)  #匹配招聘岗位名称
findArea = re.compile('<span class="t3">(.*)</span>\n<span class="t4">', re.S)  #匹配招聘地区
findComLink = re.compile(r'<span class="t2"><a.*href="(.*?)"', re.S)    #匹配公司链接
findCom = re.compile(r'<span class="t2"><a.*title="(.*?)"', re.S)   #匹配公司名称
findSalary = re.compile(r'<span class="t4">(.*?)</span>')   #匹配薪水

#获取招聘信息，公司链接、招聘岗位链接、公司名称、岗位名称、地区、薪水
#调用getCOM获取公司链接内的信息，调用getREC获取招聘岗位信息，并合并返回给main（）
def getData(bs):
    datalist = []
    for item in bs.select(".dw_table > div.el"):
        data = {}
        item = str(item)

        link = re.findall(findLink, item)
        data['link'] = ''.join(link)

        title = re.findall(findTitle, item)
        data['title'] = ''.join(title)

        area = re.findall(findArea, item)
        data['area'] = ''.join(area)

        com = re.findall(findCom, item)
        data['com'] = ''.join(com)

        comlink = re.findall(findComLink, item)
        data['comlink'] = ''.join(comlink)

        salary = re.findall(findSalary, item)
        data['salary'] = ''.join(salary)


        strhtml = 'https://jobs.51job.com/'
        if data["link"].startswith(strhtml) and data['comlink'].startswith(strhtml):

            com_link = data['comlink']
            com_data = getCOM(com_link)
            data = dict(data.items(), **com_data)

            rec_link = data['link']
            recruit_data = getREC(rec_link)
            data = dict(data.items(), **recruit_data)
            datalist.append(data)

    return datalist


#获取公司链接内的信息，公司性质、公司规模、公司行业
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


#获取招聘岗位链接内的信息，经验、学历、招聘人数、发布日期、工作描述
def getREC(rec_link):
    jobHtml = askURL(rec_link)  #获取详情页
    bs = BeautifulSoup(jobHtml,"html.parser")

    # 经验、学历、招聘人数、发布日期
    text = bs.select(".ltype")
    job = {}
    if len(text) != 0:
        info = text[0].text.split('\xa0\xa0|\xa0\xa0')
        EDU = ['博士', '硕士', '本科', '大专',
               '中专', '中技', '高中', '初中及以下']

        job['exp'] = job['edu'] = job['other'] = job['demand'] = job['pubdate'] = " "
        for i in info:
            if '经验' in i:
                job['exp'] = i
            elif i in EDU:
                job['edu'] = i
            elif '招' in i:
                job['demand'] = i
            elif '发布' in i:
                job['pubdate'] = i
            else:
                job['other'] = i
    else:
        job['exp'] = job['edu'] = job['other'] = job['demand'] = job['pubdate'] = " "


    job['msg'] = " "
    jobMsgList = bs.select(".job_msg > p")  #工作描述
    jobMsgStr = ""
    for str in jobMsgList:
        jobMsgStr = jobMsgStr + str.text
    job["msg"] = jobMsgStr

    # jobList.append(job)
    return job


def saveDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        print(data)
        sql = '''
                insert or ignore into job_quanguo(
                link,title,comlink,com,area,salary,cp_type,cp_scale,industry,exp,edu,other,demand,pubdate,msg
                 ) 
                 values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        # print(sql)
        cur.execute(sql,(data['link'],data['title'],data['comlink'],data['com'],data['area'],data['salary'],data['cp_type'],
                         data['cp_scale'],data['industry'],data['exp'],data['edu'],data['other'],data['demand'],data['pubdate'],data['msg']))
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
            create table if not exists job_quanguo
            (
            
            link text PRIMARY KEY,
            title varchar,
            comlink text,
            com text,
            area text,
            salary text,
            cp_type text,
            cp_scale text,
            industry text,
            exp text,
            edu text,
            other text,
            demand text,
            pubdate text,
            msg text
            )
        '''
    # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

    print('Table created successfully')


if __name__ == "__main__":  # 当程序执行时
    main()
    # init_db("movietest.db")
    print("爬取完毕!")