#!/usr/bin/env python
#coding:utf-8
import unittest,requests
from util import GetXML,DB,Util

class addressTest(unittest.TestCase):
        def setUp(self):
                print("--------测试开始--------")
                xmlfile = "addressConfig.xml"
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
                self.userTable="goods_user"
                self.userValues=self.util.inivalue(self.dataBase,self.userTable,"0") 
                #初始化地址记录
                self.addressTable="goods_address"
                self.addressValues=self.util.inivalue(self.dataBase,self.addressTable,"2")
                #初始化非法操作信息
                self.myuservalue = ""
                self.addressvalues = ""

        #开始测试
        def test_address_info(self):
                for mylist in self.mylists:
                        #如果"NOT"在mylist["CheckWord"]中，建立一个数据库地址表记录
                        if ("NOT" in mylist["CheckWord"]):
                                #id从mylist["Url"]中获取
                                id = (mylist["Url"]).split("/")[4]
                                #address从mylist["CheckWord"]中获取
                                address= (mylist["CheckWord"]).split(",")[1]
                                addressvalues = id+",'"+address+"','13666666666',0"
                                self.util.insertTable(self.dataBase,self.addressTable,addressvalues)
                                #对于非法操作进行的测试
                        if ("你试图" in mylist["CheckWord"]):
                                #建立用户信息
                                self.myuservalue = "1,\"121\",\"123456\",\"12345@126.com\""
                                #建立用户信息与上面和用户关联的地址信息，id从mylist["Url"]中获取
                                id = (mylist["Url"]).split("/")[4]
                                address= "淮海中路"
                                self.addressvalues = id+",'"+address+"','13666666666',1"
                                #建立一个用户
                                self.util.insertTable(self.dataBase,self.userTable,self.myuservalue)
                                #建立一个地址
                                self.util.insertTable(self.dataBase,self.addressTable,self.addressvalues)
                        data = self.util.run_test(mylist,self.userValues,self.sign)
                        #验证返回码
                        self.assertEqual(mylist["Result"],str(data.status_code))
                        #验证返回文本
                        #如果mylist["CheckWord"]标签中存在"NOT"字符串，调用断言方法assertNotIn()
                        if "NOT" in mylist["CheckWord"]:
                                self.assertNotIn(address,str(data.text))
                        #否则调用断言方法assertIn()
                        else:
                                self.assertIn(mylist["CheckWord"],str(data.text))
                        # 如果新建成功，删除刚建立的记录
                        if "添加一个新的地址信息" in mylist["Desc"]:
                                payload = eval(mylist["InptArg"])
                                address = "\""+(str(payload["address"])).strip()+"\""
                                self.dataBase.delete(self.addressTable,"address="+address)
                        print (mylist["TestId"]+" is passsing!")

        def tearDown(self):
                #对于非法操作进行时候处理
                self.util.tearDown(self.dataBase,self.userTable,self.myuservalue)
                self.util.tearDown(self.dataBase,self.addressTable,self.addressvalues)
				#清除其他初始化信息
                self.util.tearDown(self.dataBase,self.addressTable,self.addressvalues)
                self.util.tearDown(self.dataBase,self.userTable,self.userValues)
                #关闭数据库连接
                self.dataBase.close()
                print("--------测试结束--------")


if __name__=='__main__':
        #构造测试集
        suite=unittest.TestSuite()
        suite.addTest(addressTest("test_address_info"))
        #运行测试集合
        runner=unittest.TextTestRunner()
        runner.run(suite)
