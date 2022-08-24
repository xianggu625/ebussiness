#!/usr/bin/env python
#coding:utf-8
import sqlite3,requests,hashlib
from xml.dom import minidom
import os

class GetXML(): 
        #获取测试XML文件中的测试数据
        def getxmldata(self,myXmlFile):
                dom =  minidom.parse(myXmlFile)
                self.root = dom.documentElement
                #从XML中读取数据
                TestIds = self.root.getElementsByTagName('TestId')
                Titles = self.root.getElementsByTagName('Title')
                Methods = self.root.getElementsByTagName('Method')
                Descs = self.root.getElementsByTagName('Desc')
                Urls = self.root.getElementsByTagName('Url')
                InptArgs = self.root.getElementsByTagName('InptArg')
                Results = self.root.getElementsByTagName('Result')
                CheckWords = self.root.getElementsByTagName('CheckWord')
                i = 0
                mylists=[]
                for TestId in TestIds:
                        mydicts={}
                        #获取每一个数据,形成字典
                        mydicts["TestId"] = (TestIds[i].firstChild.data).strip()
                        mydicts["Title"] = (Titles[i].firstChild.data).strip()
                        mydicts["Method"] = (Methods[i].firstChild.data).strip()
                        mydicts["Desc"] = (Descs[i].firstChild.data).strip()
                        mydicts["Url"] = (Urls[i].firstChild.data).strip()
                        if ((InptArgs[i].firstChild) is None):
                                mydicts["InptArg"] = ""
                        else:
                                mydicts["InptArg"] = (InptArgs[i].firstChild.data).strip()
                        mydicts["Result"] = (Results[i].firstChild.data).strip()
                        mydicts["CheckWord"] = (CheckWords[i].firstChild.data).strip()
                        mylists.append(mydicts)
                        i = i+1
                return mylists

                #获取测试XML文件中的是否需要登录的信息
        def getIsLogin(self,myXmlFile):
                dom =  minidom.parse(myXmlFile)
                self.root = dom.documentElement
                #从XML中读取数据
                login = self.root.getElementsByTagName('login')
                login = (str(login[0].firstChild.data)).strip()
                return login

        #获取initInfo.xml中的初始化数据
        def getUserInitInfo(self):
                dom =  minidom.parse("initInfo.xml")
                self.root = dom.documentElement
                #从XML中读取数据
                id = self.root.getElementsByTagName('id')
                id = (str(id[0].firstChild.data)).strip()
                username = self.root.getElementsByTagName('username')
                username = "\""+(str(username[0].firstChild.data)).strip()+"\""
                password = (self.root.getElementsByTagName('password'))
                password = "\""+((password[0].firstChild.data)).strip()+"\""
                email = self.root.getElementsByTagName('email')
                email = "\""+(str(email[0].firstChild.data)).strip()+"\""
                values = id +","+username+","+password+","+email
                return values   #返回的字符串values供插入数据库表goos_user中使用
                
                #获取initInfo.xml中的商品初始化数据
        def getGoodInitInfo(self):
                dom =  minidom.parse("initInfo.xml")
                self.root = dom.documentElement
                #从XML中读取数据
                goodid = self.root.getElementsByTagName('goodid')
                goodid = (str(goodid[0].firstChild.data)).strip()
                name = self.root.getElementsByTagName('name')
                name = "\""+(str(name[0].firstChild.data)).strip()+"\""
                price = self.root.getElementsByTagName('price')
                price = (str(price[0].firstChild.data)).strip()
                picture = self.root.getElementsByTagName('picture')
                picture = "\""+(str(picture[0].firstChild.data)).strip()+"\""
                desc = self.root.getElementsByTagName('desc')
                desc = "\""+(str(desc[0].firstChild.data)).strip()+"\""
                values = goodid +","+name+","+price+","+picture+","+desc
                return values   #返回的字符串values供插入数据库表goos_goods中使用

                #获取initInfo.xml中的地址初始化数据
        def getAddressInitInfo(self):
                dom =  minidom.parse("initInfo.xml")
                self.root = dom.documentElement
                #从XML中读取数据
                addressid = self.root.getElementsByTagName('addressid')
                addressid = (str(addressid[0].firstChild.data)).strip()
                address = self.root.getElementsByTagName('address')
                address = "\""+(str(address[0].firstChild.data)).strip()+"\""
                phone = self.root.getElementsByTagName('phone')
                phone = "\""+(str(phone[0].firstChild.data)).strip()+"\""
                userid = self.root.getElementsByTagName('userid')
                userid = (str(userid[0].firstChild.data)).strip()
                values = addressid +","+address+","+phone+","+userid
                return values   #返回的字符串values供插入数据库表goos_address中使用

                #获取initInfo.xml中的总订单初始化数据
        def getOrdersInitInfo(self):
                dom =  minidom.parse("initInfo.xml")
                self.root = dom.documentElement
                #从XML中读取数据
                ordersid = self.root.getElementsByTagName('ordersid')
                ordersid = (str(ordersid[0].firstChild.data)).strip()
                createtime = self.root.getElementsByTagName('createtime')
                createtime = "\""+(str(createtime[0].firstChild.data)).strip()+"\""
                status = self.root.getElementsByTagName('status')
                status = (str(status[0].firstChild.data)).strip()
                ordersaddressid = self.root.getElementsByTagName('ordersaddressid')
                ordersaddressid = (str(ordersaddressid[0].firstChild.data)).strip()
                values = ordersid +","+createtime+","+status+","+ordersaddressid
                return values   #返回的字符串values供插入数据库表goos_address中使用

                #获取initInfo.xml中的订单初始化数据
        def getOrderInitInfo(self):
                dom =  minidom.parse("initInfo.xml")
                self.root = dom.documentElement
                #从XML中读取数据
                orderid = self.root.getElementsByTagName('orderid')
                orderid = (str(orderid[0].firstChild.data)).strip()
                count = self.root.getElementsByTagName('count')
                count = (str(count[0].firstChild.data)).strip()
                ordergoodid = self.root.getElementsByTagName('ordergoodid')
                ordergoodid = (str(ordergoodid[0].firstChild.data)).strip()
                orderorderid = self.root.getElementsByTagName('orderorderid')
                orderorderid = (str(orderorderid[0].firstChild.data)).strip()
                orderuserid = self.root.getElementsByTagName('orderuserid')
                orderuserid = (str(orderuserid[0].firstChild.data)).strip()
                values = orderid +","+count+","+ordergoodid+","+orderorderid+","+orderuserid
                return values   #返回的字符串values供插入数据库表goos_address中使用
