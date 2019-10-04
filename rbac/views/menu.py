#-*- coding:utf-8 -*-

'''
菜单管理
'''

from django.shortcuts import render, redirect,reverse, HttpResponse
#from django.urls import reverse
from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm,PermissionModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')        #用户选择的一级菜单
    second_menu_id = request.GET.get('sid')        #用户选择的二级菜单

    #如果request.GET.get 中的menu_id 没有在数据库中,不显示”新建“按钮
    menu_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menu_exists:
         menu_id = None

    if menu_id:
         second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
         second_menus = []

    ################################### 权限分配 ########################################
    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()

    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:     #如果二级菜单的id存在，获取当前二级菜单下的所有权限
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)   #根据permission表中的pid_id=second_menu_id ，获取当前菜单下的所有权限
    else:
        permissions = []

    return render(request, 'rbac/menu_list.html',
                  {
                      'menus': menus,
                      'second_menus': second_menus,
                      'permissions': permissions,
                      'menu_id': menu_id,
                      'second_menu_id': second_menu_id,
                  }
            )


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

def second_menu_add(request, menu_id):
    '''
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID(用于设置默认值)
    :return:
    '''

    menu_object = models.Menu.objects.filter(id=menu_id).first()    #menu_object 直接打印是 menu。title 如 信息管理
    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})    #initial= {} 初始化赋值, menu_object, 如 信息管理
        print("form:",form)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))   #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form})   #防止表单没有输入直接点保存报错


def second_menu_edit(request, pk):
    '''
    编辑二级菜单
    :param request:
    :param pk: 当前要编辑的二级菜单
    :return:
    '''

    permission_object = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)    # 初始化赋值
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))   #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form})   #防止表单没有输入直接点保存报错


def second_menu_del(request, pk):
    '''
    删除二级菜单
    :param request:
    :return:
    '''

    url = memory_reverse(request, 'rbac:menu_list') #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)
    if request.method == 'GET':
        return render(request, 'rbac/delete.html',{'cancle':url})   #cancle 作为变量传给前端delete.html页面

    # 当点击delete.html页面的确认按钮时,浏览器向服务器发送了一个post请求，http://127.0.0.1:8000/rbac/second/menu/del/14/?_filter=mid%3D13
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)

def permission_add(request, second_menu_id):
    '''
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    '''

    if request.method == 'GET':
        form = PermissionModelForm()    #initial= {} 初始化赋值, menu_object, 如 信息管理
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择:')

        #form.instance中包含用户提交的所有值, instance
        # instance = models.Permission(title='', name='', url='', pid=second_menu_object)
        # instance.pid = second_menu_object 相当于给instance 增加 pid=second_menu_object
        # instance.save()

        form.instance.pid = second_menu_object
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))   #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form})   #防止表单没有输入直接点保存报错

def permission_edit(request, pk):
    '''
    编辑二级菜单
    :param request:
    :param pk: 当前要编辑的二级菜单
    :return:
    '''

    permission_object = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)    # 初始化赋值
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))   #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)

    return render(request, 'rbac/change.html', {'form': form})   #防止表单没有输入直接点保存报错


def permission_del(request, pk):
    '''
    删除二级菜单
    :param request:
    :return:
    '''

    url = memory_reverse(request, 'rbac:menu_list') #重定向到带原始参数的URL(通过URL参数反向解析得到带参的URL)
    if request.method == 'GET':
        return render(request, 'rbac/delete.html',{'cancle':url})   #cancle 作为变量传给前端delete.html页面

    # 当点击delete.html页面的确认按钮时,浏览器向服务器发送了一个post请求，http://127.0.0.1:8000/rbac/second/menu/del/14/?_filter=mid%3D13
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


import re
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string    #根据字符串形式导入模块，这句话不太明白
#from django.urls import RegexURLResolver, RegexURLPattern     #此处与视频中一样
from django.urls.resolvers import URLPattern, URLResolver       #此处与视频中不一样


def check_url_exclude(url):
    '''
    排除特定的URL
    :param url:
    :return:
    '''
    # exclude_url = [
    #     '/admin/.*',
    #     '/login/.*',
    # ]
    #exclude_url 这个列表放在settings.py中了
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True

def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    '''
    递归的去获取URL(前提是url必须有name别名)
    :param pre_namespace: namespace的前缀， 以后用于拼接name
    :param pre_url: url前缀，以后用于拼接URL
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有的路由
    :return:
    '''
    for item in urlpatterns:
        if isinstance(item, URLPattern):   #非路由分发，将路由添加到url_ordered_dict
            if not item.name:  #如果当前URL没有别名name,则跳过当前URL，向后处理
                continue

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            #url = pre_url + item._regex  注意：item._regex 表示当前URL,可能不存在
            print("pre_url:",pre_url)
            url = pre_url + str(item.pattern)    # /^rbac/^user/edit/(?P<pk>\d+)/$， str(item.pattern)表示当前URL的字符串形式, 本案例中 /^rbac/  是pre_url

            #运行报错：'URLResolver' object has no attribute 'regex'
            url = url.replace('^', '').replace('$', '')   #得到 /rbac/user/edit/(?P<pk>\d+)/
            if check_url_exclude(url):
                continue

            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):   #路由分发，递归操作
            if pre_namespace:
                if item.namespace:      #namespace 也可能有多级
                    namespace = "%s:%s" % (pre_namespace, item.namespace)   #包括父级namespace, 和当前级namespace
                else:
                    namespace = pre_namespace   #视频中这句好像打错了，namespace = item.namespace, 应该namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            #recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)  #这行是原始视频代码：item.regex.pattern 表示URL前缀 + 当前URL
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)  #pre_url + item.regex.pattern 表示URL前缀 + 当前URL

def get_all_url_dict():
    '''
    获取项目中所有的URL
    :return:
    '''
    url_ordered_dict = OrderedDict()
    '''
    {
       'rbac: menu_list': { name: 'rbac:menu_list', url: 'xxx/xxx/menu_list'}
    }
    '''
    #在settings.py中 ROOT_URLCONF = 'luffy_permission.urls'
    md = import_string(settings.ROOT_URLCONF)   #from luff... import urls  根据字符串形式导入一个模块
    #print("md:", md)   #md: <module 'luffy_permission.urls' from 'D:\\lufei_xue_cheng\\module7\\crm\\luffy_permission\\luffy_permission\\urls.py'>
    #print("md.urlpatterns:", md.urlpatterns)  #返回如下 4行内容 ,注意：URLResolver 与 URLPattern
    # md.urlpatterns: [
    # <URLResolver <URLPattern list> (admin:admin) 'admin/'>,
    # <URLResolver <module 'rbac.urls' from 'D:\\lufei_xue_cheng\\module7\\crm\\luffy_permission\\rbac\\urls.py'> ([rbac]:rbac) '^rbac/'>,
    # <URLResolver <module 'web.urls' from 'D:\\lufei_xue_cheng\\module7\\crm\\luffy_permission\\web\\urls.py'> (None:None) '^'>]

    #None 表示根路由没有分发，namespace没有前缀。 '/', 表示在根路由前面 加/
    recursion_urls(None,'/', md.urlpatterns, url_ordered_dict)   #递归去获取所有的路由
    return url_ordered_dict

def multi_permissions(request):
    '''
    批量操作权限
    :param request:
    :return:
    '''
    #获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    #print("all_url_dict:",all_url_dict)
    for k,v in all_url_dict.items():
        print(k,v)

    '''
    输出结果：
rbac:role_list {'name': 'rbac:role_list', 'url': '/rbac/role/list/'}
rbac:role_add {'name': 'rbac:role_add', 'url': '/rbac/role/add/'}
rbac:role_edit {'name': 'rbac:role_edit', 'url': '/rbac/role/edit/(?P<pk>\\d+)/'}
rbac:role_del {'name': 'rbac:role_del', 'url': '/rbac/role/del/(?P<pk>\\d+)/'}
rbac:user_list {'name': 'rbac:user_list', 'url': '/rbac/user/list/'}
rbac:user_add {'name': 'rbac:user_add', 'url': '/rbac/user/add/'}
rbac:user_edit {'name': 'rbac:user_edit', 'url': '/rbac/user/edit/(?P<pk>\\d+)/'}
rbac:user_del {'name': 'rbac:user_del', 'url': '/rbac/user/del/(?P<pk>\\d+)/'}
rbac:user_reset_pwd {'name': 'rbac:user_reset_pwd', 'url': '/rbac/user/reset/password/(?P<pk>\\d+)/'}
rbac:menu_list {'name': 'rbac:menu_list', 'url': '/rbac/menu/list/'}
rbac:menu_add {'name': 'rbac:menu_add', 'url': '/rbac/menu/add/'}
rbac:menu_edit {'name': 'rbac:menu_edit', 'url': '/rbac/menu/edit/(?P<pk>\\d+)/'}
rbac:menu_del {'name': 'rbac:menu_del', 'url': '/rbac/menu/del/(?P<pk>\\d+)/'}
rbac:second_menu_add {'name': 'rbac:second_menu_add', 'url': '/rbac/second/menu/add/(?P<menu_id>\\d+)/'}
rbac:second_menu_edit {'name': 'rbac:second_menu_edit', 'url': '/rbac/second/menu/edit/(?P<pk>\\d+)/'}
rbac:second_menu_del {'name': 'rbac:second_menu_del', 'url': '/rbac/second/menu/del/(?P<pk>\\d+)/'}
rbac:permission_add {'name': 'rbac:permission_add', 'url': '/rbac/permission/add/(?P<second_menu_id>\\d+)/'}
rbac:permission_edit {'name': 'rbac:permission_edit', 'url': '/rbac/permission/edit/(?P<pk>\\d+)/'}
rbac:permission_del {'name': 'rbac:permission_del', 'url': '/rbac/permission/del/(?P<pk>\\d+)/'}
rbac:multi_permissions {'name': 'rbac:multi_permissions', 'url': '/rbac/multi/permissions/'}
customer_layout {'name': 'customer_layout', 'url': '/layout'}
    '''
    return HttpResponse('...')