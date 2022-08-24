#!/usr/bin/env python
#coding:utf-8
import sqlite3,requests,hashlib
from xml.dom import minidom
import os
from GetXML import GetXML

class Util:
        def __init__(self):
                self.url = "http://127.0.0.1:8000"
                self.s = requests.session()
 
        #SHA256加密
        def sha256(self,value):
                value=str(value)
                hsobj = hashlib.sha256()
                hsobj.update(value.encode("utf-8"))
                return hsobj.hexdigest()
                
        #初始化信息
        def inivalue(self,dataBase,ordertable,sign):
                #获得初始化信息
                if sign == "0":
                        values = GetXML.getUserInitInfo(self)
                elif sign == "1":
                        values = GetXML.getGoodInitInfo(self)
                elif sign == "2":
                        values = GetXML.getAddressInitInfo(self)
                elif sign == "3":
                        values = GetXML.getOrdersInitInfo(self)
                elif sign == "4":
                        values = GetXML.getOrderInitInfo(self)
                else:
                        print("sign is error in function inivalue")
                #建立记录
                if(sign!="0"):
                        self.insertTable(dataBase,ordertable,values)
                #处理在用户注册的时候，需要将密码SHA256加密处理
                else:
                        dom =  minidom.parse("initInfo.xml")
                        self.root = dom.documentElement
                        password = self.root.getElementsByTagName('password')
                        password = str(password[0].firstChild.data).strip()
                        md5password = self.sha256(password)
                        newvalues = values.replace(password,md5password)
                        self.insertTable(dataBase,ordertable,newvalues)
                return values
                
                
        #插入数据
        #dataBase为数据库
        #table为数据库
        #values为值
        def insertTable(self,dataBase,table,values):
                #获取插入数据的id
                id = values.split(',')[0].strip("\"")
                #连接数据库
                dataBase.connect()
                #查询数据库表中是否存在中
                if dataBase.searchByid(table,id):
                        #如果存在，删除这条记录
                        dataBase.delete(table,"id="+id)
                #插入测试所需要的用户
                dataBase.insert(table,values)

        #运行测试接口
        # mylist测试数据
        # values登录数据
        def run_test(self,mylist,values,sign):
                #获取测试URL
                Login_url = self.url+"/login_action/" #login_Url为登录的URL
                run_url = mylist["Url"] #run_url为运行测试用例所需的URL
                #获取csrf_token
                data = self.s.get(Login_url)
                csrf_token = data.cookies["csrftoken"]
                #初始化登录变量
                #获取登录数据
                username = values.split(',')[1].strip("\"")
                password = values.split(',')[2].strip("\"")
                password = self.sha256(password)
                #判断当前测试是否需要登录
                if not(sign==0):
                        #使用当前用户登录系统
                        payload ={"username":username,"password":password,"csrfmiddlewaretoken":csrf_token}
                        try:
                                data = self.s.post(Login_url,data=payload)
                        except Exception as e:
                                print(e)
                #运行测试接口
                try:
                        #为POST请求,由于post请求参数肯定是存在的，所以这里不判断有无参数
                        if mylist["Method"] == "post":
                                payload = eval(mylist["InptArg"])
                                #如果不是测试CSRF的
                                if mylist["Result"]!="403":
                                        payload["csrfmiddlewaretoken"] = csrf_token
                                if "password" in payload:
                                        password=self.sha256(payload["password"])
                                        payload["password"] = password
                                if "oldpassword" in payload:
                                        password=self.sha256(payload["oldpassword"])
                                        payload["oldpassword"] = password
                                if "newpassword" in payload:
                                        password=self.sha256(payload["newpassword"])
                                        payload["newpassword"] = password
                                if "checkpassword" in payload:
                                        password=self.sha256(payload["checkpassword"])
                                        payload["checkpassword"] = password
                                data = self.s.post(run_url,data=payload)
                        #为GET请求
                        elif mylist["Method"] == "get":
                                if mylist["InptArg"]=="":
                                        data = self.s.get(run_url)
                                else:
                                        payload = eval(mylist["InptArg"])
                                        print(payload)
                                        data = self.s.get(run_url,params=payload)
                except Exception as e:
                        print(e)
                else:
                        return data

        def initChart(self):
                data = self.s.get(self.url+"/remove_chart_all/")
        
        def tearDownByCookie(self):
                data = self.s.get(self.url+"/remove_chart/0/")
        
        def tearDown(self,dataBase,table,values):
                #获取初始化数据库中的记录主码
                id = values.split(',')[0]
                if len(id)!=0:
                        #删除这条记录
                        dataBase.delete(table,"id="+id)
