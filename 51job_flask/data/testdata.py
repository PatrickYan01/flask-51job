#-*- coding = utf-8 -*-
#@Time : 2020/5/24 21:13
#@Author : Patrick
#@File : testdata.py
#@Software: PyCharm

import sqlite3
import pandas as pd

area = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = "SELECT area FROM job_quanguo "
area = cur.execute(sql)
data = ""
area_data = pd.DataFrame(columns=('name','value'))
for item in area:
    data = str(''.join(item).split('-')[0:1])
    area_data = area_data.append([{'name':data,'value':1}], ignore_index=True)
cur.close()
con.close()

df = area_data.groupby('name').count().reset_index()
area_num = df.to_dict(orient='records')
df.to_csv("area_num.csv",encoding="gbk")




















# area_num = []
# con = sqlite3.connect("51job.db")
# cur = con.cursor()
# sql = "SELECT area as name, count(area) as value FROM job_quanguo " \
#       "GROUP BY area"
# area_num = cur.execute(sql)
# for item in area_num:
#     print(item)
#     # area_num=dict(item.items(), **item)
# cur.close()
# con.close()
#
# # print(area_num)