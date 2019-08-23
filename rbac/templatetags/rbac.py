
#-*- coding:utf-8-*-
# 这个文件名可以是任意名称

import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict

register = Library()    # 这个对象名必须叫register

#inclusion_tag('模板路径')
@register.inclusion_tag('rbac/static_menu.html')    #'rbac/static_menu.html' 是以luffy_permission\rbac\templates 作为根目录
def static_menu(request):
    '''
    创建一级菜单
    :return:
    '''
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list }


#inclusion_tag('模板路径')
@register.inclusion_tag('rbac/multi_menu.html')    #'rbac/multi_menu.html' 是以luffy_permission\rbac\templates 作为根目录
def multi_menu(request):
    '''
    创建二级菜单
    :return:
    '''
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    """
    menu_dict形如：
{
    1:
     {
        'title': '信息管理',
        'icon': 'fa-camero-retro',
         'children': [
             {'title': '客户列表', 'url': '/customer/list/'}
         ]
     },
    2: {
        'title': '用户管理',
        'icon': 'fa-fire',
        'children': [
            {'title': '账单列表', 'url': '/payment/list/'}
        ]
    }
}
    """

    #sorted() 对字典的key进行排序, 1, 2, ...
    key_list = sorted(menu_dict)

    #创建一个空的有序字典
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            regex = "^%s$" % (per['url'],)
            if re.match(regex, request.path_info):
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    """
在字典中添加了key, 'class': 'hide' 隐藏标签， key: 'class': 'active' 使用当前标签处于活动状态
{
    1:
     {
        'title': '信息管理',
        'icon': 'fa-camero-retro',
        'class': '',
         'children': [
             {'title': '客户列表', 'url': '/customer/list/', 'class': 'active'}
         ]
     },
    2: {
        'title': '用户管理',
        'icon': 'fa-fire',
         'class': 'hide',
        'children': [
            {'title': '账单列表', 'url': '/payment/list/'}
        ]
    }
}
    """

    return {'menu_dict': ordered_dict}