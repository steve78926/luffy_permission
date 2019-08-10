
from django.urls import re_path, path
from web.views import customer, payment

urlpatterns = [
    re_path(r'layout', customer.layout),
    re_path(r'customer/list/$', customer.customer_list),
    re_path(r'customer/add/$', customer.customer_add),
    re_path(r'cumtomer/edit/(?P<cid>\d+)/$', customer.customer_edit),
    re_path(r'customer/del/(?P<cid>\d+)/$', customer.customer_del),
]

