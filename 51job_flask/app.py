from flask import Flask,render_template,request
import sqlite3
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/index')
def index():
    return render_template("home.html")


@app.route('/company')
def comapany():

    return render_template("company.html")


@app.route('/beijing')
def comapany_beijing():
    datalist_beijing = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT * FROM job_beijing"
    data_beijing = cur.execute(sql)
    for item in data_beijing:
        datalist_beijing.append(item)
    cur.close()
    con.close()

    return render_template("company_beijing.html", jobs_beijing=datalist_beijing)

@app.route('/shanghai')
def comapany_shanghai():
    datalist_shanghai = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT * FROM job_shanghai"
    data_shanghai = cur.execute(sql)
    for item in data_shanghai:
        datalist_shanghai.append(item)
    cur.close()
    con.close()

    return render_template("company_shanghai.html", jobs=datalist_shanghai)

@app.route('/guangzhou')
def comapany_guangzhou():
    datalist_guangzhou = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT * FROM job_guangzhou"
    data_guangzhou = cur.execute(sql)
    for item in data_guangzhou:
        datalist_guangzhou.append(item)
    cur.close()
    con.close()

    return render_template("company_guangzhou.html", jobs=datalist_guangzhou)

@app.route('/shenzhen')
def comapany_shenzhen():
    datalist_shenzhen = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT * FROM job_shenzhen"
    data_shenzhen = cur.execute(sql)
    for item in data_shenzhen:
        datalist_shenzhen.append(item)
    cur.close()
    con.close()

    return render_template("company_shenzhen.html", jobs=datalist_shenzhen)

@app.route('/chengdu')
def comapany_chengdu():
    datalist_chengdu = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT * FROM job_chengdu"
    data_chengdu = cur.execute(sql)
    for item in data_chengdu:
        datalist_chengdu.append(item)
    cur.close()
    con.close()

    return render_template("company_hangzhou.html", jobs=datalist_chengdu)


@app.route('/analysis')
def analysis():
    data_area = []
    data_salary = []
    con = sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "SELECT area,round(avg(mean_salary),1) FROM job_salary " \
          "GROUP BY area ORDER BY avg(mean_salary) DESC"
    datalist = cur.execute(sql)
    arealist = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '合肥', '西安', '南京', '苏州',
                '重庆', '长沙', '佛山', '宁波', '福州', '东莞', '无锡', '昆明', '青岛', '沈阳', '南通', '厦门']
    for item in datalist:
        area = ''.join(item[0])
        if area in arealist:
            data_area.append(item[0])    #地区
            data_salary.append(item[1])    #平均薪水
        else:
            continue
    cur.close()
    con.close()

    return render_template("analysis.html", data_area=data_area,data_salary=data_salary)


if __name__ == '__main__':
    app.run()
