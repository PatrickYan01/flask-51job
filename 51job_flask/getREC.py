#-*- coding = utf-8 -*-
#@Time : 2020/5/28 15:42
#@Author : Patrick
#@File : getCP.py
#@Software: PyCharm


import sqlite3
import numpy as np

data_cp_type = []
data_salary = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = "SELECT pubdate, count(link) as num FROM job_quanguo " \
      "WHERE pubdate != ' ' " \
      "GROUP BY pubdate ORDER BY pubdate ASC "
datalist = cur.execute(sql)
for item in datalist:
    print('{value:'+str(item[1])+',name:"'+ str(item[0].replace("发布","")) +'"},')
    data_cp_type.append(item)
cur.close()
con.close()

print(data_cp_type)
print(len(data_cp_type))