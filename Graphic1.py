# python 画柱状图和折线图
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# 执行查询语句:
year = []
total = []
male = []
female = []
mratio = []
fratio = []
for i in range(0, 20):                        # 获取二十年的数据
    cursor.execute('select * from population where year=?', (2018 - i,))
    values = cursor.fetchall()
    print(values[0])
    year.append(values[0][0])
    total.append(values[0][1])
    male.append(values[0][2])
    female.append(values[0][3])
    mratio.append(float(100*values[0][2])/float(values[0][1]))
    fratio.append(float(100 * values[0][3]) / float(values[0][1]))
    print(float(values[0][2])/float(values[0][3]))
# 倒一下顺序，画出来更好看:
year.reverse()
total.reverse()
male.reverse()
female.reverse()
mratio.reverse()
fratio.reverse()

cursor.close()
conn.close()

l = [i for i in range(len(year))]      # 年份范围

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签

fmt = '%.2f%%'
yticks = mtick.FormatStrFormatter(fmt)  # 设置百分比形式的坐标轴
fig = plt.figure(figsize=(9, 6))     # 设置图的大小
ax1 = fig.add_subplot(111)  # 1X1，位置1
ax1.plot(l, mratio, 'ob-', label=u'男性比例')
ax1.plot(l, fratio, 'or-', label=u'女性比例')
ax1.yaxis.set_major_formatter(yticks)
ax1.set_ylim([48, 52])    # 比例范围
ax1.set_ylabel('比例')
plt.xlabel('年份')
plt.legend(prop={'family': 'SimHei', 'size': 8}, loc="upper left")   # 设置中文

ax2 = ax1.twinx()  # ax2为条形图，使用twinx就可以把柱状图和条形图画在一张图上了
plt.bar(l, total, alpha=0.3, color='blue', label=u'人口数(万)')
ax2.set_ylim([125000, 141000])  # 设置y轴取值范围
ax2.set_ylabel('人口数量（万）')
plt.legend(prop={'family': 'SimHei', 'size': 8}, loc="upper right")   # legend的字体和位置

plt.xticks(l, year)
plt.xticks(rotation=60)
plt.title(u'近二十年中国人口', fontsize='large', fontweight='bold')
plt.show()
