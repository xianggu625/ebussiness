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
from django.conf.urls import url
from django.contrib import admin
from goods import views	
from django.views import static

urlpatterns = [
	url(r'^$', views.index),
	url(r'^index/$', views.index),
	url(r'^admin/', admin.site.urls),
	url(r'^logout/$', views.logout),
	url(r'^register/$', views.register),
	url(r'^user_info/$', views.user_info),
	url(r'^login_action/$', views.login_action),
	url(r'^search_name/$', views.search_name),
    url(r'^change_password/$', views.change_password),
	url(r'^goods_view/$', views.goods_view),
	url(r'^view_goods/(?P<good_id>[0-9]+)/$', views.view_goods),
	url(r'^view_chart/$', views.view_chart),
	url(r'^remove_chart_all/$', views.remove_chart_all),
	url(r'^remove_chart/(?P<good_id>[0-9]+)/$', views.remove_chart),
	url(r'^add_chart/(?P<good_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.add_chart),
	url(r'^update_chart/(?P<good_id>[0-9]+)/$', views.update_chart),
	url(r'^view_address/$', views.view_address),
	url(r'^add_address/(?P<sign>[0-9]+)/$', views.add_address),
	url(r'^delete_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$',views.delete_address),
	url(r'^update_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.update_address),
	url(r'^delete_orders/(?P<orders_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.delete_orders),
	url(r'^create_order/$', views.create_order),
	url(r'^view_order/(?P<orders_id>[0-9]+)/$', views.view_order),
	url(r'^view_all_order/$', views.view_all_order),
	url(r'^upload/(?P<path>.*)',static.serve,{'document_root':'C:\\Users\\Jerry\ebusiness\\upload'}),
]
