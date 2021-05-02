#-*- coding = utf-8 -*-
#@Time : 2020/5/29 17:35
#@Author : Patrick
#@File : getwordcloud.py
#@Software: PyCharm

import jieba
import re

import sqlite3
import numpy as np

word = []
con = sqlite3.connect("51job.db")
cur = con.cursor()
sql = " SELECT msg FROM job_quanguo" \
      " WHERE msg != ''  "
datalist = cur.execute(sql)
for item in datalist:
    word.append(item)
cur.close()
con.close()

#转成字符串格式，并将所有字母转化为大写，方便分析
t = ''.join(('%s' %w for w in word))
t = t.upper()

#清除无关内容（序号、特殊符号等）
pattern = re.compile(r'\d[．|\.|、]')
pattern1 = re.compile(r'\s')
t = re.sub(pattern,'', t)
t = re.sub(pattern1, '', t)
for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~【】◆，；、。（）':
    t = t.replace(ch, "")
t = t.replace('\xa0','')

#使用jieba库分词
words = jieba.lcut(t)
counts = {}
for word in words:
    counts[word] = counts.get(word,0) + 1

#给分词字典添加技能类词汇，方便识别
ls_add = 'SQL,PYTHON,SPSS,TABLEAU,OFFICE,EXCEL,PPT,HADOOP,JAVA,R,SAS,SPARK,HIVE,WORD,ABTEST,MYSQL,MATLAB'.split(',')
for i in ls_add:
    jieba.add_word(i)

#不断调整，删除无关字符
excludes = {'的','和','等','有','数据','分析','及','及','对','并','数据分析','相关','优先',
           '能力','进行','与','熟悉','要求','使用','需求','团队','以上','负','熟练','或','良好','以上学历',
           '年','公司','为','任','专业','具备','能','提供','具有','项目','互联网','者','支持','挖掘','模型',
            '建模','能够','强','具','统计','开发','了解','监控','设计','大','中','应用','指标','建议','建立',
            '客户','根据','完成','通过','研究','体系','管理','行为','技术','平台','部门','较','提出','参与'
            ,'较','较强','软件','3','推动','掌握','基于','一定','理解','从','精通','合','2','至少','包括','发展',
            '协助','搭建','一种','语言','优秀','资格','以及','在','各','熟练掌握','常用','处理','深入','落地','敏感度'
            ,'结果','发现','方向','日常','数据处理','1','善于','指定','流程','精神','机器','快速','提升',
           '方法','海量','系统','敏感','制定','其他','核心','各类','整理','建设','构建','协','输出','定期','完善',
           '基础','提取','有效','实现','信息','方案','我们','运用','背景','针对','解决','活动','深度','你','如'
            ,'结合','专业本科','解决方案','领域','给出','改进','专题','维护','驱动','跟踪','及时','编写','形成','规划',
           '场景','考虑','实际','新','框架','操','清晰','实施','5','机会','可','将','情况','类','特征'
            }
for word in excludes:
    del counts[word]



# 获取技能
'''
ls_add = 'SQL,PYTHON,SPSS,TABLEAU,OFFICE,EXCEL,PPT,HADOOP,JAVA,R,SAS,SPARK,HIVE,WORD,ABTEST,MYSQL,MATLAB'.split(',')
ls_num = []
for i in ls_add:
    ls_num.append(t.count(i))
ls = list(zip(ls_add, ls_num))
ls.sort(key = lambda x:x[1],reverse=True)
ls_tec,ls_count = zip(*ls)


print(ls_tec) #技能，R没能正确爬取。。
print(ls_count) #次数

'''