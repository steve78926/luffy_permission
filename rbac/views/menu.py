#-*- coding:utf-8 -*-

'''
菜单管理
'''

from django.shortcuts import render, redirect,reverse, HttpResponse
#from django.urls import reverse
from rbac import models
from rbac.forms.menu import MenuModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')
    return render(request, 'rbac/menu_list.html', {'menus': menus, 'menu_id': menu_id })


def menu_add(request):
    '''
    添加一级菜单
    :param request:
    :return:
    '''

    if request.method == 'GET':
        form = MenuModelForm()
        print('form:', form)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))   #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form})   #防止表单没有输入直接点保存报错


def menu_edit(request, pk):
    '''
    编辑一级菜单
    :param request:
    :return:
    '''

    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = MenuModelForm(instance=obj)   #因为有instance=obj ，所以表单中有默认值
        return render(request, 'rbac/change.html', {'form': form})   #访问http://127.0.0.1:8000/rbac/role/edit/1/， 表单中有默认值

    form = MenuModelForm(instance=obj, data=request.POST)  #data=request.POST 表示提交过来的数据
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))  #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form })    #错误信息的展示 防止表单没有输入直接点保存报错
    ######## 上一行代码不能是redirect(), 必须是render()  ############


def menu_del(request, pk):
    '''
    删除一级菜单
    :param request:
    :return:
    '''

    url = memory_reverse(request, 'rbac:menu_list') #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)
    if request.method == 'GET':
        return render(request, 'rbac/delete.html',{'cancle':url})   #cancle 作为变量传给前端delete.html页面

    # 当点击delete.html页面的确认按钮时,浏览器向服务器发送了一个post请求，url:http://127.0.0.1:8000/rbac/role/del/7/
    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)