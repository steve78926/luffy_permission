from django.db import models

# Create your models here.

class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    role = models.ManyToManyField(verbose_name='关联的角色', to='Role', blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    '''
    角色表
    '''
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='关联的权限',to='Permission',blank=True)

    def __str__(self):
        return self.title


class Permission(models.Model):
    '''
    权限表
    '''
    title = models.CharField(verbose_name='权限名称', max_length=64)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    def __str__(self):
        return self.title
