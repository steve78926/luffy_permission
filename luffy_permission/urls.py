"""luffy_permission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),    #如果是路由分发，则实例化生成 RegexURLResolver 对象
    re_path(r'^rbac/', include('rbac.urls', namespace='rbac')),  #如果是路由分发，则实例化生成 RegexURLResolver 对象
    re_path(r'^', include('web.urls')),   #如果是路由分发，则实例化生成 RegexURLResolver 对象
]
