# -*- coding: utf-8 -*-
# filename: mydb.py


# 导入pymysql
import pymysql

# 连接数据库
conn = pymysql.connect(
         host="localhost",
         port=3306,  #端口号, 默认为3306
         user="root",
         password="Li256374819@mysql",
         db="wechat",   # 填写你设置的数据库名称
         charset="utf8")

# 创建一个可执行SQL语句的游标
cursor = conn.cursor()

"""
# new table:
sql = \"""
CREATE TABLE content (
id INT auto_increment PRIMARY KEY ,
keyword VARCHAR(20) NOT NULL ,
reply VARCHAR(100) NOT NULL 
)ENGINE=innodb DEFAULT CHARSET=utf8;
\"""
# 执行SQL语句
cursor.execute(sql)

# 关闭光标对象
cursor.close()

# 关闭数据库连接
conn.close()
"""



# SQL插入语句
sql = 'insert into content(keyword, reply) values(%s, %s);'

# 三组关键字回复
data = [
    ('资源', '这是关键字“资源”的回复内容'),
    ('123', '这是关键字“123”的回复内容'),
    ('abc', '这是关键字“abc”的回复内容')
]

# 拼接并执行sql语句
cursor.executemany(sql, data)

# 涉及写操作要注意提交
conn.commit()

# 关闭连接
cursor.close()
conn.close()

# 查询：
"""
# 查询语句
sql = 'SELECT keyword,reply FROM content;'

# 执行SQL
cursor.execute(sql)

# 取值
datas = cursor.fetchall()
# datas里面就包含了三条数据
"""