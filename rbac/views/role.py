#-*- coding:utf-8 -*-

'''
角色管理
'''

from django.shortcuts import render
from rbac import models


def role_list(request):
    '''
    角色列表
    :param request:
    :return:
    '''
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles': role_queryset})  #role_list.html 在luffy_permission\rbac\templates\rbac 下

def role_add(request):
    '''
    添加角色
    :param request:
    :return:
    '''
    return render(request, 'rbac/role_add.html')