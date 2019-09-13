#-*- coding:utf-8 -*-

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from rbac.views import role

app_name = '[rbac]'         # 启动遇到报错 'Specifying a namespace in include() without providing an app_name '，添加此行
urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),  #在html中引用时格式：名称空间：url别名，如rbac:role_list
    re_path(r'^role/add/$', role.role_add, name='role_add'),  #在html中引用时格式：名称空间：url别名，如rbac:role_add
]
