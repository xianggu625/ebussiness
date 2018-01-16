#!/usr/bin/env python
#coding:utf-8
import sqlite3,requests,hashlib
from xml.dom import minidom

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
                password = self.root.getElementsByTagName('password')
                password = "\""+(str(password[0].firstChild.data)).strip()+"\""
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



class DB:
        #构造函数，获得sqlite3数据库文件的位置
        def __init__(self):
                self.url = "C:\\Users\\Jerry\\ebusiness\\db.sqlite3"

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

class Util:
        def __init__(self):
                self.url = "http://127.0.0.1:8000"
                self.s = requests.session()
        
        #MD5加密
        def md5(self,mystr):
                if isinstance(mystr,str):
                        m = hashlib.md5()   
                        m.update(mystr.encode('utf8'))
                        return m.hexdigest()
                else:
                        return ""
		
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
                #处理在用户注册的时候，需要将密码MD5处理
                else:
                        dom =  minidom.parse("initInfo.xml")
                        self.root = dom.documentElement
                        password = self.root.getElementsByTagName('password')
                        password = str(password[0].firstChild.data).strip()
                        md5password = self.md5(password)
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
                #判断当前测试是否需要登录
                if sign:
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
                                data = self.s.post(run_url,data=payload)
                        #为GET请求
                        elif mylist["Method"] == "get":
                                if mylist["InptArg"]=="":
                                        data = self.s.get(run_url)
                                else:
                                        payload = eval(mylist["InptArg"])
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
                #删除这条记录
                dataBase.delete(table,"id="+id)
