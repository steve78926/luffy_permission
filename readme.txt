2019-07-30 :

报错：

启动luffy_permission项目时，遇到如下报错：

 File "D:\lufei_xue_cheng\module7\crm\luffy_permission\web\urls.py", line 3, in <module>
    from web.views import customer, payment
ImportError: cannot import name 'customer'

原因：在web目录下，有一个目录是views,其下有customer.py 和 payment.py， 另外，还有一个文件是views.py

D:\lufei_xue_cheng\module7\crm\luffy_permission\web\urls.py 在执行from web.views import customer, payment  时

不知道是从views目录里导入，还是从views.py里导入。

解决： 移除web目录下的views.py，正常启动项目