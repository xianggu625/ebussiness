#!/usr/bin/env python
#coding:utf-8
import unittest,requests
from GetXML import GetXML
from DB import DB
from util import Util

class goodTest(unittest.TestCase):
        def setUp(self):
                print("--------测试开始--------")
                xmlfile = "goodsConfig.xml"
                #建立GetXML对象变量
                xmlInfo = GetXML()
                #获得是否需要登录的信息
                self.sign = xmlInfo.getIsLogin(xmlfile)
                #获得所有测试数据
                self.mylists = xmlInfo.getxmldata(xmlfile)
                #建立DB变量
                self.dataBase = DB()
                #建立util变量
                self.util =Util()
                #初始化用户记录
                self.userTable = "goods_user"
                self.userValues = self.util.inivalue(self.dataBase,self.userTable,"0")    
                #初始化商品记录
                self.goodsTable = "goods_goods"
                self.goodsValues = self.util.inivalue(self.dataBase,self.goodsTable,"1")


        #开始测试
        def test_goods_info(self):
                for mylist in self.mylists:
                        data = self.util.run_test(mylist,self.userValues,self.sign)
                        print("data")
                        print(data)
                        #验证返回码
                        self.assertEqual(mylist["Result"],str(data.status_code))
                        #验证返回文本
                        #如果mylist["CheckWord"]标签中存在"NOT"字符串，调用断言方法assertNotIn()
                        if "NOT" in mylist["CheckWord"]:
                                self.assertNotIn((mylist["CheckWord"]).split(",")[1],str(data.text))
                        #否则调用断言方法assertIn()
                        else:
                                self.assertIn(mylist["CheckWord"],str(data.text))
                        print (mylist["TestId"]+" is passsing!")

        def tearDown(self):
                self.util.tearDown(self.dataBase,self.goodsTable,self.goodsValues)
                self.util.tearDown(self.dataBase,self.userTable,self.userValues)
                #关闭数据库连接
                self.dataBase.close()
                print("--------测试结束--------")


if __name__=='__main__':
        #构造测试集
        suite=unittest.TestSuite()
        suite.addTest(goodTest("test_goods_info"))
        #运行测试集合
        runner=unittest.TextTestRunner()
        runner.run(suite)
