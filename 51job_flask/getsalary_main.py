#-*- coding = utf-8 -*-
#@Time : 2020/5/24 23:12
#@Author : Patrick
#@File : getsalary_main.py
#@Software: PyCharm

import sqlite3
import numpy as np

data_area = []
data_salary = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = "SELECT area,round(avg(mean_salary),1) FROM job_salary " \
      "GROUP BY area ORDER BY avg(mean_salary) DESC"
datalist = cur.execute(sql)
arealist = ['北京','上海','广州','深圳','杭州','成都','武汉','合肥','西安','南京','苏州',
            '重庆','长沙','佛山','宁波','福州','东莞','无锡','昆明','青岛', '沈阳','南通','厦门']
for item in datalist:
    area = ''.join(item[0])
    if area in arealist:
        data_area.append(item[0])  # 地区
        data_salary.append(item[1])  # 平均薪水
    else:
        continue
cur.close()
con.close()

print(data)

