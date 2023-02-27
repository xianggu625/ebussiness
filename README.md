# ebussiness
This is the programe of ebusiness written by Django   
1）download these code  
2）install python 3.7+  
3）pip3 install Django==4.1.6  
4) run runserver.bat  
5) open brower,enter http://127.0.0.1:8000  
#转换为MySQL支持  
1.	安装书上的介绍安装完毕ebusines数据库是放在SQLite上的，下面来介绍如何让ebusiness支持MySQL  
2.	修改ebusiness/ebusiness/settings.py  
…  
# Database  
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases  
  
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'ebusiness',  
        'USER': 'root',  
        'PASSWORD': '123456',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',  
    }  
}  
…  
这里root的密码为123456。  
3.	在MySQL数据库中建立ebusiness数据库。  
4.	下载python插件mysql  
pip3 install pymysq  
5.	在ebusiness目录下运行如下命令：  
/ebusiness>python manage.py makemigrations goods  
/ebusiness>python manage.py migrate  
6.	查看数据库，应该出现如下的表：  
7.	将本目录中的goods_goods.sql、goods_user.sql导入到ebusiness数据库中（或者用两个csv文件导入）。
