
from django.urls import re_path, path
from web.views import customer, payment

urlpatterns = [
    re_path(r'layout', customer.layout),
]

