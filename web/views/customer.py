
from django.shortcuts import render, redirect
from web import models
from web.forms.customer import CustomerForm


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
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer/list')
    return render(request, 'customer_add.html', {'form': form})


def customer_edit(request, cid):
    '''
    编辑客户
    :param request:
    :param cid:
    :return:
    '''
    obj = models.Customer.objects.filter(id=cid).first()
    form = CustomerForm(instance=obj)       #注意，这里必须写成CustomerForm(instance=obj)(看源码方法要求), 如果写成位置参数 CustomerForm(obj) 会报错 ''Customer' object has no attribute 'get''
    if request.method == 'POST':
        form = CustomerForm(data=request.POST,instance=obj)    #注意，这里必须是一个关键字参数，否则，如果这样写CustomerForm(request.POST,obj)，form.save是增加记录，而不是修改
        if form.is_valid():
            form.save()
            return redirect('customer/list')
    return render(request, 'customer_edit.html', {'form': form})


def customer_del(request, cid):
    '''
    删除客户
    :param request:
    :param cid:
    :return:
    '''
    models.Customer.objects.filter(id=cid).delete()
    return redirect('/customer/list')

def layout(request):
    '''
    layout test
    :param request:
    :return:
    '''
    return render(request, 'layout.html')