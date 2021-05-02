#-*- coding = utf-8 -*-
#@Time : 2020/5/27 16:02
#@Author : Patrick
#@File : del_data.py
#@Software: PyCharm

import sqlite3

con = sqlite3.connect("51job.db")
cur = con.cursor()
table_name = "job_salary"
sql = "Delete From {0} Where com='上海苗焕实业有限公司' and title='高级数据挖掘分析师'".format(table_name)
cur.execute(sql)
cur.close()
con.close()