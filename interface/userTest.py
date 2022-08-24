#!/usr/bin/env python
#coding:utf-8
import unittest,requests
from GetXML import GetXML
from DB import DB
from util import Util

class userTest(unittest.TestCase):
        def setUp(self):
                print("--------测试开始--------")
                xmlfile = "userInfoConfig.xml"
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

        #开始测试
        def test_user_info(self):
                for mylist in self.mylists:
                        data = self.util.run_test(mylist,self.userValues,self.sign)
                        #验证返回码
                        self.assertEqual(mylist["Result"],str(data.status_code))
                        #验证返回文本
                        self.assertIn(mylist["CheckWord"],str(data.text))
                        print (mylist["TestId"]+" is passsing!")

        def tearDown(self):
                self.util.tearDown(self.dataBase,self.userTable,self.userValues)
                #关闭数据库连接
                self.dataBase.close()
                print("--------测试结束--------")


if __name__=='__main__':
        #构造测试集
        suite=unittest.TestSuite()
        suite.addTest(userTest("test_user_info"))
        #运行测试集合
        runner=unittest.TextTestRunner()
        runner.run(suite)
