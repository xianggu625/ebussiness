#!/usr/bin/env python
#coding:utf-8
import unittest,requests
from util import GetXML,DB,Util

class orderTest(unittest.TestCase):
        def setUp(self):
                print("--------测试开始--------")
                xmlfile = "orderConfig.xml"
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
                #初始化地址记录
                self.addressTable = "goods_address"
                self.addressValues = self.util.inivalue(self.dataBase,self.addressTable,"2")
                #初始化总订单记录
                self.ordersTable = "goods_orders"
                self.ordersValues = self.util.inivalue(self.dataBase,self.ordersTable,"3")
                #初始化订单记录
                self.orderTable = "goods_order"
                self.orderValues = self.util.inivalue(self.dataBase,self.orderTable,"4")
                #初始化非法操作信息
                self.myuservalue = ""
                self.myordervalues = ""
                self.myordersvalues = ""

        #开始测试
        def test_order_info(self):
                for mylist in self.mylists:
                        if ("你试图" in mylist["CheckWord"]):
                                #建立用户信息
                                self.myuservalue = "1,\"121\",\"123456\",\"12345@126.com\""
                                #建立用户信息与上面和用户关联的单个订单和总订单，id从mylist["Url"]中获取
                                id = (mylist["Url"]).split("/")[4]
                                self.myordervalues = id+",2,0,"+id+",1"
                                self.myordersvalues = id+",\"Sept. 13, 2017, 3:55 a.m.,\",0,0"
                                #建立一个用户
                                self.util.insertTable(self.dataBase,self.userTable,self.myuservalue)
                                #建立一个总订单
                                self.util.insertTable(self.dataBase,self.ordersTable,self.myordersvalues)
                                #建立一个单个订单
                                self.util.insertTable(self.dataBase,self.orderTable,self.myordervalues)
                        data = self.util.run_test(mylist,self.userValues,self.sign)
                        #验证返回码
                        self.assertEqual(mylist["Result"],str(data.status_code))
                        #验证返回文本
                        #如果mylist["CheckWord"]标签中存在"NOT"字符串，调用断言方法assertNotIn()
                        if "NOT" in mylist["CheckWord"]:
                                self.assertNotIn((mylist["CheckWord"]).split(",")[1],str(data.text))
                                #建立单独订单记录
                                self.util.insertTable(self.dataBase,self.ordersTable,self.ordersValues)
                                #建立总订单记录
                                self.util.insertTable(self.dataBase,self.orderTable,self.orderValues)
                        #否则调用断言方法assertIn()
                        else:
                                self.assertIn(mylist["CheckWord"],str(data.text))
                        #如果是验证查看全部订单，测试完毕把测试数据删除
                        if "view_all_order" in mylist["Url"]:
                                self.dataBase.delete(self.ordersTable,"status='0'")
                                self.dataBase.delete(self.orderTable,"count=1")
                        print (mylist["TestId"]+" is passsing!")

        def tearDown(self):
                #对于非法操作进行时候处理
                self.util.tearDown(self.dataBase,self.userTable,self.myuservalue)
                self.util.tearDown(self.dataBase,self.orderTable,self.myordervalues)
                self.util.tearDown(self.dataBase,self.ordersTable,self.myordersvalues)
                #删除setup建立的单个订单
                self.util.tearDown(self.dataBase,self.orderTable,self.orderValues)
                #删除setup建立的总订单
                self.util.tearDown(self.dataBase,self.ordersTable,self.ordersValues)
                #删除setup建立的地址
                self.util.tearDown(self.dataBase,self.addressTable,self.addressValues)
                #删除setup建立的商品
                self.util.tearDown(self.dataBase,self.goodTable,self.goodValues)
                #删除setup建立的用户
                self.util.tearDown(self.dataBase,self.userTable,self.userValues)
                #关闭数据库连接
                self.dataBase.close()
                print("--------测试结束--------")


if __name__=='__main__':
        #构造测试集
        suite=unittest.TestSuite()
        suite.addTest(orderTest("test_order_info"))
        #运行测试集合
        runner=unittest.TextTestRunner()
        runner.run(suite)
