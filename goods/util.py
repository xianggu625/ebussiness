#coding=utf-8
from django.shortcuts import render,get_object_or_404
from goods.models import Goods,Address,Order,Orders,User
from goods.object import Chart_list,Order_list,Orders_list
import hashlib


# 以下是类模型定义部分
class Util:
    #检查用户是否登录
    def check_user(self,request):
        #从session中取出username
        username = str(request.session.get('username',''))
        #判断数据库中是否存在
        user = User.objects.filter(username = username)
        #如果不存在，返回空串
        if (user is None):
            return ""
        #否则返回username
        else:
            return username

	
    #通过addressId判断这个地址是否属于当前登录用户
    def check_User_By_Address(self,request,username,addressId):
        #获取addressId对应的address信息
        address = get_object_or_404(Address,id=addressId)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if address.user_id ==user.id:
            return 1
        else:
            return 0

    #通过orderId判断这个订单是否属于当前登录用户
    def check_User_By_Order(self,request,username,orderId):
        #获取orderId对应的order信息
        order = get_object_or_404(Order,id=orderId)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if order.user_id ==user.id:
            return 1
        else:
            return 0

    #通过ordersId判断这个地址是否属于当前登录用户
    def check_User_By_Orders(self,request,username,orderId):
        #获取orderId对应的orders信息
        orders = get_object_or_404(Orders,id=orderId)
        #获取orders.id对应的order信息
        order = Order.objects.filter(order_id=orders.id)
        #通过username获取对应的user信息
        user = get_object_or_404(User,username=username)
        #判断addressId对应的userid与username获取对应的userid是否相等
        if len(order)>0:
            if order[0].user_id == user.id:
                return 1
        else:
            return 0

    def is_number(self,s):
        try:
            int(s)
            return True
        except ValueError:
            pass
        return False

    #返回购物车内商品的个数
    def cookies_count(self,request):
        #返回本地所有的cookie
        cookie_list = request.COOKIES
        length = 0
        #只要进入网站，系统中就会产生一个名为sessionid的cookie
        #如果后台同时在运行，会产生一个名为csrftoken的cookie
        for i in cookie_list:
            if (self.is_number(i)):
                length = length+1
        return length

    #获取购物车内的所有内容
    def deal_cookes(self,request):
        #获取本地所有内COOKIES
        cookie_list = request.COOKIES
        #如果COOKIES内不是数值，去除
        for key in list(cookie_list.keys()):
            if not (self.is_number(key)):
                del cookie_list[key]
        #返回处理好的购物车内的所有内容
        return cookie_list

    #加入购物车
    def add_chart(self,request):
        #获取购物车内的所有内容
        cookie_list = self.deal_cookes(request)
        #定义my_chart_list列表
        my_chart_list = []
        #遍历cookie_list，把里面的内容加入类Chart_list列my_chart_list中
        for key in cookie_list:
            chart_object = Chart_list
            chart_object = self.set_chart_list(key,cookie_list)
            my_chart_list.append(chart_object)
        #返回 my_chart_list
        return my_chart_list


    #定义单个订单变量
    def set_order_list(self,key):
        order_list = Order_list()
        order_list.set_id(key.id)#主键
        good_list = get_object_or_404(Goods,id=key.goods_id)#获得当前商品信息
        order_list.set_good_id(good_list.id)#订单中商品编号
        order_list.set_name(good_list.name)#订单中商品名字
        order_list.set_price(good_list.price)#订单中商品价格
        order_list.set_count(key.count)#购买数量
        return order_list

    def set_orders_list(self,key):
        order_list = Orders_list()
        order_list.set_id(key.id)#主键
        order_list.set_address(key.address)#地址信息
        order_list.set_create_time(key.create_time)#创建时间
        return order_list

    #把获取的购物车中的商品放在一个名为Chart_list()的类中，返回给模板
    def set_chart_list(self,key,cookie_list):
        chart_list = Chart_list()
        good_list = get_object_or_404(Goods, id=key)
        chart_list.set_id(key)#商品的标号
        chart_list.set_name(good_list.name)#商品的名称
        chart_list.set_price(good_list.price)#商品的价钱
        chart_list.set_count(cookie_list[key])#商品的个数
        return chart_list

    #时间格式转换
    def time_format(self,t):
        t1=["","","",""]
        t = t.replace('.',' ')
        t = t.split(" ")
        d = t[0].split("-")
        t1[0] = d[0]+"年"
        t1[1] = d[1]+"月"
        t1[2] = d[2]+"日"
        t1[3] = t[1]
        t1 = " " .join(t1)
        return t1
