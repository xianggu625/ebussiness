#!/usr/bin/env python
#coding:utf-8
from util import DB,Util

if __name__=='__main__':
        dataBase = DB()
        util =Util()
        for id in range(10,100):
                goodvaluse = str(id)+",'测试产品',126.50,'upload/1.jpg','测试产品'"
                util.insertTable(dataBase,'goods_goods',goodvaluse)
