
from django.shortcuts import render, redirect
from web import models

def customer_list(request):
    '''
    客户列表
    :param request:
    :return:
    '''
    data_list = models.Customer.objects.all()
    return render(request, 'customer_list.html', {'data_list': data_list})


def customer_add(request):
    '''
    添加客户
    :param request:
    :return:
    '''
    

def layout(request):
    '''
    layout test
    :param request:
    :return:
    '''
    return render(request, 'layout.html')