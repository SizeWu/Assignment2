# 爬取近几年大中型企业申请专利数，插入表patent，再获取，绘图
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# 执行查询语句: 查询相应年份专利申请数
year = []
patent = []
for i in range(1, 8):
    cursor.execute('select * from patent where year=?', (2018 - i,))
    values = cursor.fetchall()
    print(values[0])
    year.append(int(values[0][0]))
    patent.append(int(values[0][1]))
cursor.close()
conn.close()

# 倒一下顺序，画出来更好看:
year.reverse()
patent.reverse()


conn = sqlite3.connect('data.db')
cursor = conn.cursor()
patentnum = []

for i in range(0, 20):
    cursor.execute('select * from patent2016 where type=?', (str(i),))
    values = cursor.fetchall()
    print(values)
    print(values[0])
    # type.append(int(values[0][0]))
    patentnum.append(int(values[0][1]))
cursor.close()
conn.close()
# print(patentnum)
# 以下将爬到的各类专利数量分类，放到一个新的列表patenttype里面
patenttype = []
patenttype.append(sum(patentnum[1:5]))
patenttype.append(sum(patentnum[17:20]))
patenttype.append(sum(patentnum[6:8]) + sum(patentnum[10:12]) + sum(patentnum[13:17]))
patenttype.append(sum(patentnum[8:10]) + patentnum[5] + patentnum[12])
print(patenttype)
# 将patenttype里面的数据转化成占总数的比例
typeratio = []
for value in patenttype:
    typeratio.append(value/sum(patenttype))
print(typeratio)


plt.rcParams['font.sans-serif'] = ['SimHei']     # 用来正常显示中文标签
fig = plt.figure(figsize=(14, 5))
ax1 = fig.add_subplot(131)  # 1X3，位置1
ax2 = fig.add_subplot(132)  # 1X3，位置2
ax3 = fig.add_subplot(133)
# ax1柱状图
ax1.barh(range(len(patent)), patent, color='green', tick_label=year)
ax1.set_ylabel("年份")
ax1.set_xlabel("专利数/单位（件）")
ax1.set_title("高技术产业专利申请数(大中型工业企业口径)")
'''for y, x in enumerate(patent):        # 在条形图上标出具体数据
    print('x,y:', x, y)
    # print(type(y))
    ax1.text(y-0.4, x+0.4, '%s' % x)
'''
# ax2饼状图
ax2.set_title("2016年各产业申请情况（圆饼图）")
type = [u'生物医药', u'仪器仪表', u'电子设备', u'其他']
colors = ['red', 'yellowgreen', 'orange','lightskyblue']     # 每块颜色定义
explode = (0, 0, 0, 0.05)     # 将某一块分割出来，值越大分割出的间隙越大
patches, text1, text2 = ax2.pie(typeratio,
                      explode=explode,
                      labels=type,
                      colors=colors,
                      autopct='%3.2f%%',  # 数值保留固定小数位
                      shadow=False,  # 无阴影设置
                      startangle=90,  # 逆时针起始角度设置
                      pctdistance=0.6)  # 数值距圆心半径倍数距离
# patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本

ax2.axis('equal')  # x，y轴刻度设置一致，保证饼图为圆形
ax2.legend()
# ax3柱状图
ax3.bar(range(len(patenttype)), patenttype, color=['red', 'blue', 'yellowgreen', 'orange'], tick_label=type)
ax3.set_xlabel("专利种类")
ax3.set_ylabel("专利数/单位（件）")
ax3.set_title("2016年各产业申请情况(柱状图)")
for x, y in enumerate(patenttype):        # 在条形图上标出具体数据
    print('x,y:', x, y)
    # print(type(y))
    ax3.text(x-0.4, y+0.4, '%s' % y)

plt.show()


'''
plt.figure(figsize=(9, 6))
plt.bar(range(len(patent)), patent, color='green', tick_label=year)

plt.xlabel("年份")
plt.xticks(rotation=45)
plt.ylabel("专利数/单位（件）")
plt.title("高技术产业专利申请数(大中型工业企业口径)")
for x, y in enumerate(patent):        # 在条形图上标出具体数据
    print('x,y:', x, y)
    print(type(y))
    plt.text(x-0.4, y+0.4, '%s' % y)
plt.show()
'''