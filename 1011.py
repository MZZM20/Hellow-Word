# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:11:51 2019

@author: lenovo
"""
import sys
from PyQt5 import QtSql
def create_db():
        try:
            # 调用输入框获取数据库名称
            db_text= input('数据库名称')
            db_action=True
            if (db_text.replace(' ','') != '') and (db_action is True):
                print(db_text)
                #db_name = db_text
                # 添加一个sqlite数据库连接并打开
                db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName('{}.sqlite'.format(db_text))
                db.open()
                print(db)
                # 实例化一个查询对象
                query = QtSql.QSqlQuery()
                # 创建一个数据库表
                query.exec_("create table zmister(ID int primary key, "
                            "site_name varchar(20), site_url varchar(100))")
                # 插入三条数据
                query.exec_("insert into zmister values(1000, '州的先生', 'https://zmister.com')")
                query.exec_("insert into zmister values(1001, '百度', 'http://www.baidu.com')")
                query.exec_("insert into zmister values(1002, '腾讯', 'http://www.qq.com')")
                print('创建数据库成功')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    #创建应用程序和对象
    create_db();