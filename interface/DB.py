#!/usr/bin/env python
#coding:utf-8
import sqlite3,requests,hashlib
from xml.dom import minidom
import os

class DB:
        #构造函数，获得sqlite3数据库文件的位置
        def __init__(self):
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.url = BASE_DIR+"\\db.sqlite3"

        #连接数据库连接
        def connect(self):
                self.con = con = sqlite3.connect(self.url)
                self.cur = self.con.cursor()


        #关闭数据库连接
        def close(self):
                self.cur.close()
                self.con.close()

        #通过主键查询数据库表中的内容
        def searchByid(self,tablename,id):
                return(self.cur.execute("select * from "+tablename+" where id="+id))
                
        #向tablename表中插入数据values
        def insert(self,tablename,values):
                sql = "insert into "+tablename+" values ("+values+")"
                self.con.execute(sql)
                self.con.commit()

        #在tablename表，删除满足condtion条件的记录
        def delete(self,tablename,condition):
                sql = "delete from "+tablename+" where "+condition
                self.con.execute(sql)
                self.con.commit()
