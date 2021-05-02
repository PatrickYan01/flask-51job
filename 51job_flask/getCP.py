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
sql = " SELECT industry, count(DISTINCT com) as num FROM job_salary " \
      " WHERE industry LIKE '%互联网/电子商务%'  "
datalist = cur.execute(sql)
for item in datalist:
    print('{value:'+str(item[1])+',name:"'+ str(item[0]) +'"},')
    data_cp_type.append(item)
cur.close()
con.close()

print(data_cp_type)
print(len(data_cp_type))