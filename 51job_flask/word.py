#-*- coding = utf-8 -*-
#@Time : 2020/5/20 11:40
#@Author : Patrick
#@File : word.py
#@Software: PyCharm


import jieba
from matplotlib import pyplot as plt
from wordcloud  import WordCloud
from PIL import Image
import numpy as np
import sqlite3
import os.path

#准备词云所需的词
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "51job.db")
con = sqlite3.connect(db_path)
cur = con.cursor()
sql = 'SELECT msg FROM job_quanguo WHERE area LIKE "%深圳%"'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
# print(text)
cur.close()
con.close()

#分词
cut = jieba.cut(text)
string = " ".join(cut)
# string = string.replace("任职要求","").replace("工作经验","").replace("岗位职责", "").replace("岗位要求","").replace("公司提供","")

print(string)
print(len(string))



img = Image.open(r"G:\python_work\20200516_flask\static\assets\img\tree.jpg")   #打开遮罩图
img_array = np.array(img)   #将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask= img_array,
    font_path='STZHONGS.TTF'
)
wc.generate_from_text(string)


#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')

# plt.show()
plt.savefig(r"G:\python_work\20200518_51job_flask\static\assets\img\word.jpg", dpi=2000)