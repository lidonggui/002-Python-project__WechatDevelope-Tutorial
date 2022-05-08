# -*- coding: utf-8 -*-
# filename: mydb.py

import pymysql
from dbutils.pooled_db import PooledDB
# we use dbutils==2.0.1 , and with the sentence "from dbutils.pooled_db import PooledDB"

# 建立连接池
pool = PooledDB(pymysql, 5, # 连接池pool里面按照要求填写，里面有个数字“5”，这里指的是设定5条连接数，你可以根据需求增加
            host="localhost", 
            user='root',
            passwd='Li256374819@mysql', 
            db='wechat', 
            port=3306, 
            charset="utf8")


# 添加函数
def addcontent(data):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = 'insert into content(keyword, reply) values(%s, %s);'
    try:
        cursor.executemany(sql, data)
        conn.commit()
        print('添加成功')
    except Exception as e:
        print(str(e))
        # 有异常就回滚
        conn.rollback()
    cursor.close()
    conn.close()


# 查询函数
def mycontent(key):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute('select keyword, reply from content where keyword=%s', key)
    alldata = cursor.fetchone()  # 将数据库的数据（元组嵌套）赋值给datas
    data = alldata[1]  # we use the second worlds !
    cursor.close()
    conn.close()
    return data


if __name__ == "__main__":
    data = [('你是谁？', '我是李东洋！'),
            ('你好', '你好呀！')]
    addcontent(data)