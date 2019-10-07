#-*- coding:utf-8 -*-

'''
组合菜单的例子
'''

menu_list = [
    { 'id':1, 'title': '菜单1'},
    { 'id':2, 'title': '菜单2'},
    { 'id':3, 'title': '菜单3'},

]
menu_dict = {}

for item in menu_list:
    menu_dict[item['id']] = item

'''
{
    1:{ id:'1', 'title': '菜单1'},
    2:{ id:'2', 'title': '菜单2'},
    3:{ id:'3', 'title': '菜单3'},
}

'''
menu_dict[2]['title'] = '666'

#修改了menu_dict, 但menu_list 也发生了变化   为什么？ 答：menu_list 与 menu_dict 是指向同一块内存地址

menu_dict[2]['children'] = [11,22]
print(menu_list)  #[{'id': 1, 'title': '菜单1'}, {'id': 2, 'title': '666', 'children': [11, 22]}, {'id': 3, 'title': '菜单3'}]