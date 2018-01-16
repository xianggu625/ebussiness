#coding=utf-8
# 以下是类模型定义部分
#购物车模型
class Chart_list():
    #主键
    def set_id(self,id):
        self.id=id

    #商品名称
    def set_name(self,name):
        self.name=name

    #商品价格
    def set_price(self,price):
        self.price=price

    #商品数量
    def set_count(self,count):
        self.count=count
        
#订单模型
class Order_list():
    #订单编号
    def set_id(self,id):
        self.id=id

    #订单中商品编号
    def set_good_id(self,good_id):
        self.good_id=good_id

    #订单中商品名称
    def set_name(self,name):
        self.name=name

    #订单中商品价钱
    def set_price(self,price):
        self.price=price

    #订单中商品数量
    def set_count(self,count):
        self.count=count

    #商品总价钱（个数*单价）
    def set_prices(self,prices):
        self.prices=prices


#总订单模型
class Orders_list():
    #总订单编号
    def set_id(self,id):
        self.id=id

    #总订单收货地址
    def set_address(self,address):
        self.address=address

    #总订单建立时间
    def set_create_time(self,create_time):
        self.create_time=create_time