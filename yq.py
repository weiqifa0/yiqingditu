import time
import json
import requests
import jsonpath
from pyecharts.charts import Map
import pyecharts.options as opts


# 全国疫情地区分布(各省确诊病例)
def catch_cn_disease_dis():
    timestamp = '%d'%int(time.time()*1000)
    url_area = ('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
               '&callback=&_=') + timestamp
    world_data = json.loads(requests.get(url=url_area).json()['data'])
    china_data = jsonpath.jsonpath(world_data,
                                   expr='$.areaTree[0].children[*]')
    ls_province_names = jsonpath.jsonpath(china_data, expr='$[*].name')
    ls_confirm_vals = jsonpath.jsonpath(china_data, expr='$[*].total.confirm')
    ls_province_confirm = list(zip(ls_province_names, ls_confirm_vals,))
    return ls_province_confirm, world_data


ls_province_cfm, dic_world_data = catch_cn_disease_dis()
print(ls_province_cfm)

# 绘制全国疫情地图
def map_cn_disease_dis() -> Map:
    c = (
        Map()
        .add('中国', ls_province_cfm, 'china')
        .set_global_opts(
            title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
            visualmap_opts=opts.VisualMapOpts(is_show=True,
                                              split_number=6,
                                              is_piecewise=True,  # 是否为分段型
                                              pos_top='center',
                                              pieces=[
                                                   {'min': 10000, 'color': '#7f1818'},  #不指定 max
                                                   {'min': 1000, 'max': 10000},
                                                   {'min': 500, 'max': 999},
                                                   {'min': 100, 'max': 499},
                                                   {'min': 10, 'max': 99},
                                                   {'min': 0, 'max': 5} ],
                                              ),
        )
    )
    return c
map_cn_disease_dis().render('全国疫情地图.html')