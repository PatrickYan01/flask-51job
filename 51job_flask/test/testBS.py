#-*- coding = utf-8 -*-
#@Time : 2020/5/18 15:13
#@Author : Patrick
#@File : testBS.py
#@Software: PyCharm
#
# from bs4 import BeautifulSoup
#
# html = open("job.html", "r")
# bs = BeautifulSoup(html, "html.parser")
#
# jnames = bs.select(".in > .cn > h1")
# # print(jnames[0]["title"])  # 岗位名称
#
# cnameList = bs.select(".cname > a")[0]["title"]  # 公司名称
# # print(cnameList)
# salary = bs.select(".cn strong")[0].get_text()  # 薪水
# # print(salary)
#
# jobMsgList = bs.select(".job_msg > p")  # 工作描述
# jobMsgStr = ""
# for str in jobMsgList:
#     jobMsgStr = jobMsgStr + str.text


# days = bs.select(".ltype")
# info = days[0].text.split("|")
# job["area"] = info[0].strip()  # 地区
# job["experience"] = info[1].strip()  # 经验
# job["edu"] = info[2].strip()  # 学历
# job["num"] = info[3].strip()  # 招聘人数
# job["date"] = info[4].strip()  # 发布日期



link = "https://jobs.51job.com/shenzhen-ftq/111629606.html?s=01&t=0"

str = 'https://jobs.51job.com/'
print(link.startswith(str) )