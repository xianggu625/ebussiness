#!/usr/bin/env python
#coding:utf-8
import unittest,requests
from util import GetXML,DB,Util

class charttest(unittest.TestCase):
        def setUp(self):
                print("--------测试开始--------")
                xmlfile = "chartConfig.xml"
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
                self.goodTable = "goods_goods"
                self.goodValues = self.util.inivalue(self.dataBase,self.goodTable,"1")

        #开始测试
        def test_chart_info(self):
                #初始化购物车，把购物车中所有内容均删除
                data = self.util.initChart()
                for mylist in self.mylists:  
                        data = self.util.run_test(mylist,self.userValues,self.sign)
                        #验证返回码
                        self.assertEqual(mylist["Result"],str(data.status_code))
                        #如果mylist["CheckWord"]标签中存在"NOT"字符串，调用断言方法assertNotIn()
                        if "NOT" in mylist["CheckWord"]:
                                self.assertNotIn((mylist["CheckWord"]).split(",")[1],str(data.text))
                        #否则调用断言方法assertIn()
                        else:
                                self.assertIn(mylist["CheckWord"],str(data.text))
                        print (mylist["TestId"]+" is passsing!")

        def tearDown(self):
                #删除cookie
                self.util.tearDownByCookie()
                #删除setup建立的商品
                self.util.tearDown(self.dataBase,self.goodTable,self.goodValues)
                #删除setupo建立的用户
                self.util.tearDown(self.dataBase,self.userTable,self.userValues)
                #关闭数据库连接
                self.dataBase.close()
                print("--------测试结束--------")


if __name__=='__main__':
        #构造测试集
        suite=unittest.TestSuite()
        suite.addTest(charttest("test_chart_info"))
        #运行测试集合
        runner=unittest.TextTestRunner()
        runner.run(suite)
