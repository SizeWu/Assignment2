# 采用requests库,获取专利数量的数据
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
    # 目标网址(问号前面的东西)
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
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0N0T01"}]'
    keyvalue['k1'] = str(gettime())

    # 发出请求，使用get方法，这里使用我们自定义的头部和参数
    r = requests.post(url, headers=headers, params=keyvalue)
    # 打印返回过来的状态码
    print(r.status_code)
    # 打印我们构造的url
    print(r.url)
    # 打印返回的数据
    # print(r.text)
    return json.loads(r.text)    # 返回json格式

'''
data = getstat()
print(type(data))
print(data)
print(data['returndata']['datanodes'][0])
print(type(data['returndata']['datanodes'][0]['wds'][1]['valuecode']))
print(data['returndata']['datanodes'][1]['wds'][1]['valuecode'])          # 年份
print(data['returndata']['datanodes'][1]['data']['strdata'])              # 数据/单位（件）
'''