from django.db import models


# Create your models here.

class Customer(models.Model):
    '''
    客户表
    '''
    name = models.CharField(verbose_name='客户名称', max_length=32)
    agent = models.CharField(verbose_name='年龄', max_length=4)
    email = models.EmailField(verbose_name='邮箱', max_length=20)
    company = models.CharField(verbose_name='公司名称', max_length=32)

    def __str__(self):
        return self.name


class Payment(models.Model):
    '''
    付费记录
    '''
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer', on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now_add=True)
