# 采用requests库，获取人口数据
import requests
import time
import json


# 用来获取 时间戳
def gettime():
    return int(round(time.time() * 1000))


def getstat():
    # 用来自定义头部的
    headers = {}
    # 用来传递参数的
    keyvalue = {}
    # 目标网址
    url = 'http://data.stats.gov.cn/easyquery.htm'

    # 头部的填充
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) ' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                            'Version/12.0 Safari/605.1.15'

    # 下面是参数的填充
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = str(gettime())

    # 建立一个Session
    s = requests.session()
    # 在Session基础上进行一次请求,使用post方法，这里使用我们自定义的头部和参数
    r = s.post(url, params=keyvalue, headers=headers)
    # 打印返回过来的状态码
    print(r.status_code)
    # 修改dfwds字段内容
    keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'
    # 再次进行请求
    r = s.post(url, params=keyvalue, headers=headers)
    # 此时我们就能获取到我们搜索到的数据了
    # print(r.text)
    return json.loads(r.text)     # 返回json格式
