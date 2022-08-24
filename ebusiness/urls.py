"""ebusiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.conf.urls import url
from django.urls import re_path
from django.contrib import admin
from goods import views	
from django.views import static
import os
from django.conf.urls.static import static
from . import settings
from django.conf import settings
from django.views.static import serve

urlpatterns = [
	re_path(r'^$', views.index),
	re_path(r'^index/$', views.index),
	re_path(r'^admin/', admin.site.urls),
	re_path(r'^logout/$', views.logout),
	re_path(r'^register/$', views.register),
	re_path(r'^user_info/$', views.user_info),
	re_path(r'^login_action/$', views.login_action),
	re_path(r'^search_name/$', views.search_name),
        re_path(r'^change_password/$', views.change_password),
	re_path(r'^goods_view/$', views.goods_view),
	re_path(r'^view_goods/(?P<good_id>[0-9]+)/$', views.view_goods),
	re_path(r'^view_chart/$', views.view_chart),
	re_path(r'^remove_chart_all/$', views.remove_chart_all),
	re_path(r'^remove_chart/(?P<good_id>[0-9]+)/$', views.remove_chart),
	re_path(r'^add_chart/(?P<good_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.add_chart),
	re_path(r'^update_chart/(?P<good_id>[0-9]+)/$', views.update_chart),
	re_path(r'^view_address/$', views.view_address),
	re_path(r'^add_address/(?P<sign>[0-9]+)/$', views.add_address),
	re_path(r'^delete_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$',views.delete_address),
	re_path(r'^update_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.update_address),
	re_path(r'^delete_orders/(?P<orders_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.delete_orders),
	re_path(r'^create_order/$', views.create_order),
	re_path(r'^view_order/(?P<orders_id>[0-9]+)/$', views.view_order),
	re_path(r'^view_all_order/$', views.view_all_order),
]+ static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
