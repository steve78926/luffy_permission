# -*- coding:utf-8 -*-

from django.conf import settings

def init_permission(current_user, request):

    '''
    用户权限信息初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    '''
    # 2. 权限信息初始化
    #根据当前用户信息获取此用户所拥有的所有权限， 并放入session
    #  permission_list 就是当前用户所有的权限, queryset 不能直接放到session当中

    ######################   一级菜单列   ######################
    # permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
    #                                                                                   "permissions__title",
    #                                                                                   "permissions__is_menu",
    #                                                                                   "permissions__icon",
    #                                                                                   "permissions__url",
    #                                                                                   ).distinct()

    ######################   二级菜单列   ######################
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__url",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon",
                                                                                      ).distinct()

    #3. 获取权限 + 菜单信息
    # permissions__id， permissions__url 必须用双引号引起来，否则报错
    #获取权限中所有的URL
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permission_url'])

    # menu_list = []   # 一级菜单
    permission_list = []
    menu_dict = {}
    for item in permission_queryset:
        permission_list.append(item['permissions__url'])    #构建权限列表
        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue

        node = {'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)     #menu_id 是一级菜单ID, append(node) 是再次增加二级菜单项
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node,]
            }

    print(menu_dict)
    #返回：
    # {1:
    #      {
    #          'title': '信息管理',
    #         'icon': 'fa-camero-retro',
    #         'children': [
    #             {'title': '客户列表', 'url': '/customer/list/'},
    #             {'title': '账单列表', 'url': '/payment/list/'}
    #         ]
    #      }
    # }
       ############################       一级菜单   ############################
        # if item['permissions__is_menu']:
        #     temp = {                                           #构建菜单临时字典，包括，菜单名称，菜单图标，菜单URL
        #         'title': item['permissions__title'],
        #         'icon': item['permissions__icon'],
        #         'url': item['permissions__url']
        #     }
        #     menu_list.append(temp)                              #构建菜单列表

    ### permission_list = [item['permissions__url'] for item in permission_queryset]
    #request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    #request.session[settings.MENU_SESSION_KEY] = menu_list
    ############################       一级菜单代码结束   ############################
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict