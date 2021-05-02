#-*- coding = utf-8 -*-
#@Time : 2020/5/24 23:12
#@Author : Patrick
#@File : getsalary_main.py
#@Software: PyCharm

import sqlite3
import numpy as np

data_area = []
data_num = []
data_cp_num = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = "SELECT area,count(area) as num,count(DISTINCT com) as cp_num FROM job_salary " \
      "GROUP BY area ORDER BY num DESC"
datalist = cur.execute(sql)
arealist = ['北京','上海','广州','深圳','杭州','成都','武汉','合肥','西安','南京','苏州',
            '重庆','长沙','佛山','宁波','福州','东莞','无锡','昆明','青岛', '沈阳','南通','厦门']
for item in datalist:
    area = ''.join(item[0])
    if area in arealist:
        data_area.append(item[0])  # 地区
        data_num.append(item[1])  # 岗位数
        data_cp_num.append(item[2]) #公司数
    else:
        continue
cur.close()
con.close()

print(data_area)
print(data_num)
print(data_cp_num)

