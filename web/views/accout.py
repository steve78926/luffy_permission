#-*- coding:utf-8-*-

from django.shortcuts import HttpResponse, render, redirect
from rbac import models
from rbac.service.init_permission import  init_permission
#规范的代码：一个应用不应该从另外一个应用导入models, 这不符合规范

def login(request):
    '''
    :param request:
    :return:
    '''
    #1. 用户登录
    if request.method == 'GET':
        return render(request, 'login.html')

    user=request.POST.get('user')
    pwd = request.POST.get('pwd')
    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    init_permission(current_user, request)          #这里只对权限初始化部分封装， 用户登录部分不封装

    return redirect('/customer/list/')



