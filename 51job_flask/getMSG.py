#-*- coding = utf-8 -*-
#@Time : 2020/5/28 22:12
#@Author : Patrick
#@File : getMSG.py
#@Software: PyCharm


import sqlite3
import numpy as np
import numpy as np

data_cp_type = []
data_salary = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = "SELECT exp,count(exp) as num FROM job_salary " \
      "WHERE exp != ' ' GROUP BY exp ORDER BY num DESC "
datalist = cur.execute(sql)
print('------------------------')
for item in datalist:
    print('{value:'+str(item[1])+',name:"'+ str(item[0]) +'"},')
    data_cp_type.append(item)
cur.close()
con.close()

print(data_cp_type)

'''无需经验，1年经验，2年经验，3-4年经验，5-7年经验，8-9年经验，10年以上经验'''