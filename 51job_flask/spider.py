#-*- coding = utf-8 -*-
#@Time : 2020/5/18 14:26
#@Author : Patrick
#@File : spider.py
#@Software: PyCharm


import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.error,urllib.parse



jobList = []


def main():
    kw = input("请输入你要搜索的岗位关键字：").strip()
    keyword = urllib.parse.quote(urllib.parse.quote(kw))   #二次编码
    # ka = input("请输入你要搜索的地区：").strip()
    # karea = getArea(ka)

    for i in range(1, 165):
        print('正在爬取第{}页信息'.format(i))
        baseurl = "https://search.51job.com/list/"+ str(000000) +",000000,0000,00,9,99,"+ keyword +",2,"+ str(i) +".html"    #深圳+keyword
        jobLink = getLink(baseurl)
        if len(jobLink) == 0:
            break
        for jobpage in jobLink:
            datalist = getData(jobpage)
    dbpath = "./51job.db"
    saveDB(datalist, dbpath)
    print(datalist)


def getArea(ka):
    karea = " "
    if ka == "深圳":
        karea = "040000"
    elif ka == "北京":
        karea = "010000"
    elif ka == "上海":
        karea = "020000"
    elif ka == "杭州":
        karea = "080200"
    elif ka == "广州":
        karea = "030200"
    elif ka == "厦门":
        karea = "110300"
    elif ka == "福州":
        karea = "110200"
    else:
        print("地区有误")
        exit()


def getLink(baseurl):
    jobLink = []
    html = askURL(baseurl)

    bs = BeautifulSoup(html, "html.parser")
    eldiv = bs.select(".el > .t1 > span > a")

    str = 'https://jobs.51job.com/'
    for link in eldiv:
        if link["href"].startswith(str):
            jobLink.append(link["href"])
            jobList.append({"link":link["href"]})
        # print(jobList)
    return jobLink


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


def getData(jobpage):
    jobHtml = askURL(jobpage)  #获取详情页
    bs = BeautifulSoup(jobHtml,"html.parser")

    for job in jobList:
        if jobpage == job["link"]:
            jnames = bs.select(".in > .cn > h1")
            if len(jnames) != 0:
                job["title"] = jnames[0]["title"]   #岗位名称
            else:
                job["title"] = " "

            cnameList = bs.select(".cname > a")
            if len(cnameList) != 0:
                job["cname"] = cnameList[0]["title"]    #公司名称
            else:
                job["cname"] = " "


            salary = bs.select(".cn strong")
            if len(salary) != 0:
                job["salary"] = salary[0].get_text()  #薪水
            else:
                job["salary"] = " "

            # 经验、学历、招聘人数、发布日期
            days = bs.select(".ltype")
            if len(days) != 0:
                info = days[0].text.split('\xa0\xa0|\xa0\xa0')
                EDU = ['博士', '硕士', '本科', '大专',
                       '中专', '中技', '高中', '初中及以下']
                # SKILL = ['英语', '在校生/应届生', '计算机', '统计学', '学']
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
                break


            job['msg'] = " "
            jobMsgList = bs.select(".job_msg > p")  #工作描述
            jobMsgStr = ""
            for str in jobMsgList:
                jobMsgStr = jobMsgStr + str.text
            job["msg"] = jobMsgStr

    jobList.append(job)
    return jobList


def saveDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        print(data)
        sql = '''
                insert or ignore into job_quanguo(
                link,title,cname,salary,other,exp,edu,demand,pubdate,msg
                 ) 
                 values(?,?,?,?,?,?,?,?,?,?)'''
        # print(sql)
        cur.execute(sql,(data['link'],data['title'],data['cname'],data['salary'],data['other'],data['exp'],data['edu'],data['demand'],data['pubdate'],data['msg']))
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
            create table job_quanguo
            (
            
            link text PRIMARY KEY,
            cname text,
            title varchar,
            other varchar,
            salary text,
            edu text,
            exp text,
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