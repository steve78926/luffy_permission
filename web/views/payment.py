
from web import models
from django.shortcuts import render, redirect
from web.forms.payment import PaymentForm

def payment_list(request):
    '''
    打印账单
    :param request:
    :return:
    '''
    data_list = models.Payment.objects.all()
    return render(request, 'payment_list.html', {'data_list': data_list})


def payment_add(request):
    '''
    添加付费记录
    :param request:
    :return:
    '''
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(data=request.POST)
        print("form:", form)
        if form.is_valid():
            form.save()
            return redirect('/payment/list/')
    return render(request, 'payment_add.html', {'form': form})


def payment_edit(request, pid):
    '''
    编辑付费记录
    :param request:
    :return:
    '''
    obj = models.Payment.objects.get(id=pid)
    form = PaymentForm(instance=obj)
    if request.method == 'POST':
        form = PaymentForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/payment/list/')
    return render(request, 'payment_edit.html', {'form': form})


def payment_del(request, pid):
    '''
    删除付费记录
    :param request:
    :param pid:
    :return:
    '''
    models.Payment.objects.filter(id=pid).delete()
    return redirect('/payment/list/')