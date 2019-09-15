#-*- coding:utf-8 -*-

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from rbac.views import role

app_name = '[rbac]'         # 启动遇到报错 'Specifying a namespace in include() without providing an app_name '，添加此行
urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),  #在html中引用时格式：名称空间：url别名，如rbac:role_list
    re_path(r'^role/add/$', role.role_add, name='role_add'),  #在html中引用时格式：名称空间：url别名，如rbac:role_add
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),   #在html中引用时格式：名称空间：url别名，如rbac:role_edit
    re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  #如rbac:role_del
]


#访问 http://127.0.0.1:8000/rbac/role/list/# 报错如下：
#  Reverse for 'role_edit' with keyword arguments '{'pk': 1}' not found. 1 pattern(s) tried: ['rbac/role/edit/(?P<pk>\\+d)/$']
#原因：正则表达式写错： 错误写法：\+d   正确写法： \d+
 #re_path(r'^role/edit/(?P<pk>\+d)/$', role.role_edit, name='role_edit'),
