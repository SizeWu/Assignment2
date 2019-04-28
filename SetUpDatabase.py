# 爬取人口数据,在数据库data.db中，建一个table
import sqlite3
import NationalStat
import Patent

keys = ['total', 'male', 'female']


def insertdata(cursor, table, year, key, value):            # 插入数据，若存在，就更新
    try:
        cursor.execute('insert into %s (year, %s) values (%s, %s)' % (table, key, year, value))
    except sqlite3.IntegrityError:
        print('已经存在的数据，更新该数据。')
        cursor.execute('update %s set %s=? where year=? ' % (table, key), (value, year))
    else:
        print('成功插入')


def getfromnationalstat():            # 获取数据，建table
    getdata = NationalStat.getstat()
    print(type(getdata))
    print(getdata)
    conn = sqlite3.connect('data.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    try:                                              # 若已建，则提示“已被创建”
        cursor.execute('create table population (   \
                        year varchar(20) primary key,   \
                        total varchar(20),      \
                        male varchar(20),        \
                        female varchar(20))')
    except sqlite3.OperationalError:
        print('数据库已被创建！')
    else:
        print("成功创建数据库！")

    for i in range(0, 60):                                          # 将20年的数据插入table
        insertdata(cursor, 'population', getdata['returndata']['datanodes'][i]['wds'][1]['valuecode'], keys[int(i/20)],
                getdata['returndata']['datanodes'][i]['data']['strdata'])
        print(type(getdata['returndata']['datanodes'][i]['data']['strdata']))
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


def getfrompatent():
    getdata = Patent.getstat()
    conn = sqlite3.connect('data.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    try:  # 使用try,可以在已被创建时，继续运行代码
        cursor.execute('create table patent (   \
                        year varchar(20) primary key,   \
                        patent varchar(20))')
    except sqlite3.OperationalError:
        print('数据库已被创建！')
    else:
        print("成功创建数据库！")

    for i in range(0, 8):  # 最近八年
        insertdata(cursor, 'patent', getdata['returndata']['datanodes'][i]['wds'][1]['valuecode'], 'patent',
                   getdata['returndata']['datanodes'][i]['data']['data'])
        # print(type(getdata['returndata']['datanodes'][i]['data']['strdata']))
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


def getfrompatenttype():
    getdata = Patent.getstat()
    conn = sqlite3.connect('data.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    try:  # 使用try,可以在已被创建时，继续运行代码
        cursor.execute('create table patent2016 (   \
                        type varchar(20) primary key,   \
                        patentnum varchar(20))')
    except sqlite3.OperationalError:
        print('数据库已被创建！')
    else:
        print("成功创建数据库！")

    for i in range(0, 200):  # 最近八年总情况
        if getdata['returndata']['datanodes'][i]['wds'][1]['valuecode'] == '2016':
            insertdata(cursor, 'patent2016', str(int(i / 10)), 'patentnum',
                       getdata['returndata']['datanodes'][i]['data']['data'])
            # print(type(getdata['returndata']['datanodes'][i]['data']['strdata']))
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


getfromnationalstat()  # 更新人口数据
getfrompatent()        # 更新年度专利数据
getfrompatenttype()    # 更新2016年专利申请情况
