#-*- coding = utf-8 -*-
#@Time : 2020/5/26 16:55
#@Author : Patrick
#@File : getMapPie.py
#@Software: PyCharm


from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker

c = (
    Pie()
    .add("", [['上海',1174],
['广州',938],
['深圳',849],
['北京',708],

['成都',399],
['杭州',350],
['武汉',273],
['合肥',237],
['西安',231],
['南京',196],
['苏州',106],
['重庆',101],
['长沙',94],
['佛山',86],
['宁波',84],
['福州',74],
['东莞',71],
['无锡',69],
['昆明',58],
['青岛',58],
['沈阳',56],
['南通',51],
['厦门',51],
]
)
    .set_global_opts(
                     legend_opts=opts.LegendOpts(is_show=False))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}，{d}%"))
    .render("pie_base.html")
)
