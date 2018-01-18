#coding=utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from goods.models import Goods,Address,Order,Orders,User
from goods.util import Util
from goods.object import Chart_list,Order_list,Orders_list
from goods.forms import UserForm,LoginForm,AddressForm

# Create your views here.

# 以下是用户管理部分
# 首页(登录)
def index(request):
    uf = LoginForm()
    return render(request,'index.html',{'uf':uf})

#用户登出
def logout(request):
	response = HttpResponseRedirect('/index/') # 登录成功跳转查看商品信息
	del request.session['username']  # 将session 信息写到服务器
	return response

#用户注册
def register(request):
    util = Util()
    if request.method == "POST":					#判断表单是否提交状态
        uf = UserForm(request.POST)					#获得表单变量
        if uf.is_valid():						#判断表单数据是否正确
            #获取表单信息
            username = (request.POST.get('username')).strip()           #获取用户名信息
            password = (request.POST.get('password')).strip()           #获取密码信息
            #加密password
            password = util.md5(password)
            #判断密码长度是否做过50
            email = (request.POST.get('email')).strip()		#获取Email信息
            #查找数据库中是否存在相同用户名
            user_list = User.objects.filter(username=username)
            if user_list:
                #如果存在，报"用户名已经存在！"错误信息并且回到注册页面
                uf = UserForm()
                return render(request,'register.html',{'uf':uf,"error":"用户名已经存在！"})
            else:
                #否则将表单写入数据库
                user = User()
                user.username = username
                user.password = password
                user.email = email
                user.save()
                #返回登录页面
                uf = LoginForm()
                return render(request,'index.html',{'uf':uf})
    else:	#如果不是表单提交状态，显示表单信息
        uf = UserForm()
    return render(request,'register.html',{'uf':uf})


#用户登录
def login_action(request):
    util = Util()
    if request.method == "POST":
        uf = LoginForm(request.POST)
        if uf.is_valid():
            # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            #加密password
            password = util.md5(password)
            # 判断输入数据是否为空
            if username == '' or password == '':
                return render(request,"index.html",{'uf':uf,"error":"用户名和密码不能为空"})
            else:
		# 判断用户名和密码是否准确
                user = User.objects.filter(username = username,password = password)
                if user:
                    response = HttpResponseRedirect('/goods_view/') # 登录成功跳转查看商品信息
                    request.session['username'] = username    # 将session 信息写到服务器
                    return response
                else:
                    return render(request,"index.html",{'uf':uf,"error":"用户名或者密码错误"})
    else:
        uf = LoginForm()
    return render(request,'index.html',{'uf':uf})

# 获取用户信息
def user_info(request):
    #检查用户是否登录
    util = Util()
    username = util.check_user(request)
    print(username)
    #如果没有登录，跳转到首页
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入！"})
    else:
		#count为当前购物车中商品的数量
        count = util.cookies_count(request)
		#获取登录用户信息
        user_list = get_object_or_404(User,username=username)
		#获取登录用户收货地址的所有信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request,"view_user.html",{"user": username,"user_info":user_list,"address":address_list,"count":count})

# 修改用户密码
def change_password(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        count = util.cookies_count(request)
        #获得当前登录用户的用户信息
        user_info = get_object_or_404(User,username=username)
        #如果是提交表单，获取表单信息，并且进行表单信息验证
        if request.method == "POST":
            #获取旧密码
            oldpassword=util.md5((request.POST.get("oldpassword", "")).strip())
            #获取新密码
            newpassword=util.md5((request.POST.get("newpassword", "")).strip())
            #获取新密码的确认密码
            checkpassword=util.md5((request.POST.get("checkpassword", "")).strip())
            #如果旧密码不正确，报错误信息，不允许修改
            if oldpassword !=user_info.password:
                return render(request,"change_password.html",{"user": username,"error":"旧密码不正确","count":count})
            #如果新密码与旧密码相同，报错误信息，不允许修改
            elif newpassword ==oldpassword:
                return render(request,"change_password.html",{"user": username,"error":"新密码不能与旧密码相同","count":count})
            #如果新密码与新密码的确认密码不匹配，报错误信息，不允许修改
            elif newpassword != checkpassword:
                return render(request,"change_password.html",{"user": username,"error":"确认密码与新密码不匹配","count":count})
            else:
            #否则修改成功
                User.objects.filter(username=username).update(password=newpassword)
                return render(request,"change_password.html",{"user": username,"error":"密码修改成功","count":count})
        #如果不是提交表单，显示修改密码页面
        else:
            return render(request,"change_password.html",{"user": username,"count":count})
# 以下是商品管理部分
#查看商品信息
def goods_view(request):
    util = Util()
    username = util.check_user(request)
    if username =="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #获得所有商品信息
        good_list = Goods.objects.all()
        #获得购物车中物品数量
        count = util.cookies_count(request)

        #翻页操作
        paginator = Paginator(good_list, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, "goods_view.html", {"user": username, "goodss": contacts,"count":count})

# 商品搜索
def search_name(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        count = util.cookies_count(request)
        #获取查询数据
        search_name = (request.POST.get("good", "")).strip()
        print("-------------------------------------")
        print(search_name)
        #通过objects.filter()方法进行模糊匹配查询，查询结果放入变量good_list
        good_list = Goods.objects.filter(name__icontains=search_name)

        #对查询结果进行分页显示
        paginator = Paginator(good_list, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, "goods_view.html", {"user": username, "goodss": contacts,"count":count})

# 查看商品详情
def view_goods(request, good_id):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        count = util.cookies_count(request)
        good = get_object_or_404(Goods, id=good_id)
        return render(request, 'good_details.html', {"user": username,'good': good,"count":count})

# 以下是购物车管理部分
# 放入购物车
def add_chart(request,good_id,sign):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{"error":"请登录后再进入"})
    else:
        #获得商品详情
        good = get_object_or_404(Goods,id=good_id)
        #如果sign=="1"，返回商品列表页面
        if sign=="1":
            response = HttpResponseRedirect('/goods_view/')
        #否则返回商品详情页面
        else:
            response = HttpResponseRedirect('/view_goods/'+good_id)
        #把当前商品添加进购物车，参数为商品编号，值购买商品为个数1，有效时间为一年
        response.set_cookie(str(good.id),1,60*60*24*365)
        return response


# 查看购物车
def view_chart(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #购物车中商品个数
        count = util.cookies_count(request)
        #返回所有的cookie内容
        my_chart_list = util.add_chart(request)
        return render(request, "view_chart.html", {"user": username, "goodss": my_chart_list, "count":count})

# 移出购物车
def remove_chart(request,good_id):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #获取指定编号的商品
        good = get_object_or_404(Goods, id=good_id)
        response = HttpResponseRedirect('/view_chart/')
        #移除购物车
        response.set_cookie(str(good.id),1,0)
        return response

# 修改购物车中商品的数量
def update_chart(request,good_id):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
		#获取编号为good_id的商品
        good = get_object_or_404(Goods, id=good_id)
		#获取修改的数量
        count = (request.POST.get("count"+good_id, "")).strip()
		#如果数量值<=0,报出错信息
        if int(count)<=0:
			#获得购物车列表信息
            my_chart_list = util.add_chart(request)
			#返回错误信息
            return render(request, "view_chart.html", {"user": username, "goodss": my_chart_list,"error":"个数不能小与0"})
        else:
			#否则修改商品数量
            response = HttpResponseRedirect('/view_chart/')
            response.set_cookie(str(good.id),count,60*60*24*365)
            return response

# 移出购物车中所有内容
def remove_chart_all(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        response = HttpResponseRedirect('/view_chart/')
        #获取所有的购物车中的内容
        cookie_list = util.deal_cookes(request)
        #遍历购物车中的内容，一个一个地删除
        for key in cookie_list:
            response.set_cookie(str(key),1,0)
        return response

# 以下是地址管理部分
# 查看地址单
def view_address(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #返回用户信息
        user_list = get_object_or_404(User, username=username)
        #返回这个用户的地址信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request, 'view_address.html', {"user": username,'addresses': address_list})

# 添加地址
#sign=1 从用户信息进入
#sign=2 从订单信息进入
def add_address(request,sign):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf1 = LoginForm()
        return render(request,"index.html",{'uf':uf1,"error":"请登录后再进入"})
    else:
        #获得当前登录用户的所有信息
        user_list = get_object_or_404(User, username=username)
        #获得当前登录用户的编号
        id = user_list.id
        #判断表单是否提交
        if request.method == "POST":
            #如果表单提交，准备获取表单信息
            uf = AddressForm(request.POST)
            #表单信息是否正确
            if uf.is_valid():
                #如果正确，开始获取表单信息
                myaddress = (request.POST.get("address", "")).strip()
                phone = (request.POST.get("phone", "")).strip()
                #判断地址是否存在
                check_address = Address.objects.filter(address=myaddress,user_id = id)
                if not check_address:
                    #如果不存在，将表单写入数据库
                    address = Address()
                    address.address = myaddress
                    address.phone = phone
                    address.user_id = id
                    address.save()
                    #返回地址列表页面
                    address_list = Address.objects.filter(user_id=user_list.id)
                    #如果sign=="2"，返回订单信息
                    if sign=="2":
                        return render(request, 'view_address.html', {"user": username,'addresses': address_list}) #进入订单用户信息
                    else:
                    #否则返回用户信息
                        response = HttpResponseRedirect('/user_info/') # 进入用户信息
                        return response
                #否则返回添加用户界面，显示“这个地址已经存在！”的错误信息
                else:
                    return render(request,'add_address.html',{'uf':uf,'error':'这个地址已经存在！'})
        #如果没有提交，显示添加地址见面
        else:
            uf = AddressForm()
        return render(request,'add_address.html',{'uf':uf})

# 删除地址
#sign=1 从用户信息进入
#sign=2 从订单用户信息进入
def delete_address(request,address_id,sign):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        if not util.check_User_By_Address(request,username,address_id):
            return render(request,"error.html",{"error":"你试图删除不属于你的地址信息！"})
        else:
            #获取指定地址信息
            user_list = get_object_or_404(User, username=username)
            #删除这个地址信息
            Address.objects.filter(id=address_id).delete()
            #返回地址列表页面
            address_list = Address.objects.filter(user_id=user_list.id)
            #如果sign==2,返回订单信息页面
            if sign=="2":
                return render(request, 'view_address.html', {"user": username,'addresses': address_list}) #进入订单用户信息
            #否则进入用户信息页面
            else:
                response = HttpResponseRedirect('/user_info/') # 进入用户信息
                return response


# 修改地址
#sign=1 从用户信息进入
#sign=2 从订单信息进入
def update_address(request,address_id,sign):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #判断修改的地址是否属于当前登录用户
        if not util.check_User_By_Address(request,username,address_id):
            return render(request,"error.html",{"error":"你试图修改不属于你的地址信息！"})
        else:
            #获取指定地址信息
            address_list = get_object_or_404(Address, id=address_id)
            #获取当前登录用户的用户信息
            user_list = get_object_or_404(User, username=username)
            #获取用户编号
            id = user_list.id
            #如果是提交状态
            if request.method == "POST":
                #如果表单提交，准备获取表单信息
                uf = AddressForm(request.POST)
                #表单信息验证
                if uf.is_valid():
                    #如果数据准确，获取表单信息
                    myaddress = (request.POST.get("address", "")).strip()
                    phone = (request.POST.get("phone", "")).strip()
                    #判断修改的地址信息这个用户是否是否存在
                    check_address = Address.objects.filter(address=myaddress,user_id = id)
                    #如果不存在，将表单数据修改进数据库
                    if not check_address:
                        Address.objects.filter(id=address_id).update(address = myaddress,phone = phone)
                    #否则报“这个地址已经存在！”的错误提示信息
                    else:
                        return render(request,'update_address.html',{'uf':uf,'error':'这个地址已经存在！','address':address_list})
                    #获得当前登录用户的所有地址信息
                    address_list = Address.objects.filter(user_id=user_list.id)
                    #如果sign==2,返回订单信息页面
                    if sign=="2":
                        return render(request, 'view_address.html', {"user": username,'addresses': address_list}) #进入订单用户信息
                    #否则进入用户信息页面
                    else:
                        response = HttpResponseRedirect('/user_info/') # 进入用户信息
                        return response
            #如果没有提交，显示修改地址页面
            else:
                return render(request,'update_address.html',{'address':address_list})

# 以下是订单管理部分
# 生成订单
def create_order(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #根据登录的用户名获得用户信息
        user_list = get_object_or_404(User, username=username)
        #从选择地址信息中获得建立这个订单的送货地址编号
        address_id = (request.POST.get("address", "")).strip()
        #如果没有选择地址，返回错误提示信息必须选择一个地址！
        if address_id=="":
            address_list = Address.objects.filter(user_id=user_list.id)
            return render(request, 'view_address.html', {"user": username,'addresses': address_list,"error":"必须选择一个地址！"})
            #否则开始形成订单
        else:
            #把数据存入数据库中的总订单表
            orders = Orders()
            #获得订单的送货地址编号
            orders.address_id = int(address_id)
            #设置订单的状态为未付款
            orders.status = False
            #保存总订单信息
            orders.save()
            #准备把订单中的每个商品出存入单个订单表
            #获得总订单编号
            orders_id = orders.id
            #获得购物车中的内容
            cookie_list = util.deal_cookes(request)
            print("1")
            print(cookie_list)
            #遍历购物车
            for key in cookie_list:
                #构建对象Order()
                order = Order()
                #获得总订单编号
                order.order_id = orders_id
                #获得用户编号
                order.user_id = user_list.id
                #获得商品编号
                order.goods_id = key
                #获得数量
                order.count = int(cookie_list[key])
                #保存单个订单信息
                order.save()
            #清除所有cookies，并且显示这个订单
            response = HttpResponseRedirect('/view_order/'+str(orders_id))
            for key in cookie_list:
                response.set_cookie(str(key),1,0)
            return response

# 显示订单
def view_order(request,orders_id):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #获取订单信息
        orders_filter = get_object_or_404(Orders,id=orders_id)
        #获取订单的收货地址信息
        address_list = get_object_or_404(Address,id=orders_filter.address_id)
        #获取收货地址信息中的地址
        address = address_list.address
        #获得单个订单表中的信息
        order_filter = Order.objects.filter(order_id=orders_filter.id)
        #建立列表变量order_list，里面存的是每个Order_list对象
        order_list_var = []
        prices=0
        for key in order_filter:
            #定义Order_list对象
            order_object = Order_list
            #产生一个Order_list对象
            order_object =  util.set_order_list(key)
            #把当前Order_list对象加入到列表变量order_list
            order_list_var.append(order_object)
            prices = order_object.price * order_object.count + prices
        return render(request, 'view_order.html', {"user": username,'orders': orders_filter,'order': order_list_var,'address': address,"prices":str(prices)})

# 查看所有订单
def view_all_order(request):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #获得所有总订单信息
        orders_all = Orders.objects.all()
        #初始化列表，给模板
        Reust_Order_list = []
		#遍历总订单
        for key1 in orders_all:
			#通过当前订单编号获取这个订单的单个订单详细信息
            order_all = Order.objects.filter(order_id=key1.id)
            #检查这个订单是不是属于当前用户的
            user = get_object_or_404(User,id=order_all[0].user_id)
			#如果属于将其放入总订单列表中
            if user.username == username:
				#初始化总订单列表
                Orders_object_list = []
				#初始化总订单类
                orders_object = Orders_list
				#产生一个Orders_lis对象
                orders_object =  util.set_orders_list(key1)
				#初始化总价钱为0
                prices=0
				#遍历这个订单
                for key in order_all:
					#初始化订单类
                    order_object = Order_list
					#产生一个Order_lis对象
                    order_object =  util.set_order_list(key)
					#将产生的order_object类加入到总订单列表中
                    Orders_object_list.append(order_object)
					#计算总价格
                    prices = order_object.price * key.count + prices
				#把总价格放入到order_object类中
                order_object.set_prices(prices)
				#把当前记录加到Reust_Order_list列中
				#从这里可以看出，Reust_Order_list每一项是一个字典类型，key为总订单类orders_object,value为总订单列表Orders_object_list
				#总订单列表Orders_object_list中每一项为一个单独订单对象order_object，即Reust_Order_list=[{orders_object类:[order_object类,...]},...]
                Reust_Order_list.append({orders_object:Orders_object_list})
        return render(request, 'view_all_order.html', {"user": username,'Orders_set': Reust_Order_list})

# 删除订单
# id=1,3删除单个订单，id=2删除总订单
# id=1,2从查看总订单进入，id=3从查看单个订单进入
def delete_orders(request,orders_id,sign):
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf = LoginForm()
        return render(request,"index.html",{'uf':uf,"error":"请登录后再进入"})
    else:
        #如果删除单独一个订单
        if sign == "1" or sign=="3":
            #判断修改的地址是否属于当前登录用户
            if not util.check_User_By_Order(request,username,orders_id):
                return render(request,"error.html",{"error":"你试图删除不属于你的单独一个订单信息！"})
            else:
                #通过主键获得单独订单内容
                order_filter = get_object_or_404(Order,id=orders_id)
                #获得当前订单所属于的总订单
                orders_filter = get_object_or_404(Orders,id=order_filter.order_id)
                #删除这个单独订单
                Order.objects.filter(id=orders_id).delete()
                #判断这个总订单下是否还有没有商品
                judge_order = Order.objects.filter(order_id = orders_filter.id)
                #如果没有商品了
                if (len(judge_order))==0:
                    #删除这个订单所处于的总订单记录
                    Orders.objects.filter(id=orders_filter.id).delete()
                    #如果标记为3，返回商品列表页面
                    if sign=="3":
                        response = HttpResponseRedirect('/goods_view/') # 跳入商品列表页面
                    #如果标记为1，返回查看所有订单页面
                    if sign=="1":
                        response = HttpResponseRedirect('/view_all_order/') # 跳入商品列表页面
                #如果还有商品，且标记为3，返回订单确认页面
                elif sign=="3":
                    response = HttpResponseRedirect('/view_order/'+str(orders_filter.id)+'/') # 跳入订单确认
                #否则返回所有订单页面
                else:
                    response = HttpResponseRedirect('/view_all_order/') # 跳入查看所有订单
            return response
            #如果删除总订单
        elif sign == "2":
            if not util.check_User_By_Orders(request,username,orders_id):
                return render(request,"error.html",{"error":"你试图删除不属于你的总订单信息！"})
            else:
                #删除单个订单
                Order.objects.filter(order_id=orders_id).delete()
                #删除总订单
                Orders.objects.filter(id=orders_id).delete()
                #返回查看所有订单页面
                response = HttpResponseRedirect('/view_all_order/') # 跳入查看所有订单
                return response

def page_not_found(request):
	return render(request, '404.html')


def page_error(request):
	return render(request, '500.html')


def permission_denied(request):
	return render(request, '403.html')