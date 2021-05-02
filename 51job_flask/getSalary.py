#-*- coding = utf-8 -*-
#@Time : 2020/5/26 19:40
#@Author : Patrick
#@File : getSalary.py
#@Software: PyCharm

#对薪水进行数据处理

import sqlite3
import pandas as pd
import numpy as np


def getSalary():
    datalist = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT com,title,area,cp_type,cp_scale,industry,exp,edu,salary FROM job_quanguo"
    data_quanguo = cur.execute(sql)
    for item in data_quanguo:
        string = "".join(item[8])
        if string.endswith('千/月'):
            num = string.replace("千/月","").split("-")
            sal = pd.to_numeric(num)*1000
            # datalist.append(pd.to_numeric(num)*1000)
            data1 = append_other(item)
            data2 = append_salary(sal)
        elif string.endswith('万/月'):
            num = string.replace("万/月","").split("-")
            sal = pd.to_numeric(num)*10000
            # datalist.append(pd.to_numeric(num)*10000)
            data1 = append_other(item)
            data2 = append_salary(sal)
        elif string.endswith('万/年'):
            num = string.replace("万/年","").split("-")
            sal = pd.to_numeric(num)*10000/12
            # datalist.append(pd.to_numeric(num)*10000/12)
            # append_other(item)
            data1 = append_other(item)
            data2 = append_salary(sal)
        else:
            continue
        data = dict(data1.items(), **data2)
        datalist.append(data)
    cur.close()
    con.close()

    # df_salary = pd.DataFrame(columns=['low-salary','high-salary'])
    dbpath = "./51job.db"
    saveDB(datalist, dbpath)


def append_salary(sal):
    data1 = {}
    data1['low-salary'] = sal[0].astype(np.int64)
    data1['high-salary'] = sal[1].astype(np.int64)
    data1['avg-salary'] = (sal[0].astype(np.int64)+sal[1].astype(np.int64))/2

    return data1


def append_other(item):
    data2 = {}
    data2['com']=data2['title']=data2['area']=data2['cp_type']=data2['cp_scale']=data2['industry']=data2['exp']=data2['edu'] = "未知"

    data2['com'] = item[0]
    data2['title'] = item[1]
    data2['area'] = item[2].split('-')[0]
    data2['cp_type'] = item[3]
    data2['cp_scale'] = item[4]
    data2['industry'] = item[5]
    data2['exp'] = item[6]
    data2['edu'] = item[7]


    return data2


def saveDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        print(data)
        sql = '''
                insert or ignore into job_salary(
                com,title,area,cp_type,cp_scale,industry,exp,edu,low_salary,high_salary,mean_salary
                 ) 
                 values(?,?,?,?,?,?,?,?,?,?,?)'''
        # print(sql)
        cur.execute(sql, (
        data['com'], data['title'], data['area'], data['cp_type'], data['cp_scale'], data['industry'],
        data['exp'], data['edu'],data['low-salary'], data['high-salary'], data['avg-salary']))
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
            create table if not exists job_salary
            (
            com text,
            title varchar,
            area text,
            cp_type text,
            cp_scale text,
            industry text,
            exp text,
            edu text,
            low_salary NUMERIC ,
            high_salary NUMERIC ,
            mean_salary float 
            )
        '''
    # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

    print('Table created successfully')


if __name__ == '__main__':
    getSalary()
    print("处理完毕！")