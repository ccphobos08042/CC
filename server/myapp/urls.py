from django.urls import path

from myapp import views

app_name = 'myapp'
urlpatterns = [
    # api

    path('admin/loginLog/list', views.admin.loginLog.list_api),
    path('admin/loginLog/create', views.admin.loginLog.create),
    path('admin/loginLog/update', views.admin.loginLog.update),
    path('admin/loginLog/delete', views.admin.loginLog.delete),
    path('admin/opLog/list', views.admin.opLog.list_api),
    path('admin/errorLog/list', views.admin.errorLog.list_api),
    path('admin/user/list', views.admin.user.list_api),
    path('admin/user/create', views.admin.user.create),
    path('admin/user/register', views.admin.user.register),
    path('admin/user/update', views.admin.user.update),
    path('admin/user/updatePwd', views.admin.user.updatePwd),
    path('admin/user/delete', views.admin.user.delete),
    path('admin/user/info', views.admin.user.info),
    path('admin/adminLogin', views.admin.user.admin_login),


    path('admin/jingju/list',views.admin.jingju.list_api),
    path('admin/jingju/create',views.admin.jingju.create),
    path('admin/jingju/update',views.admin.jingju.update),
    path('admin/jingju/delete',views.admin.jingju.delete),
    path('admin/jingju/yolov8',views.admin.jingju.yolov8),
    path('admin/jingju/opendoor',views.admin.jingju.opendoor),

    path('admin/jingjucabinet/list',views.admin.jingjucabinet.list_api),
    path('admin/jingjucabinet/create',views.admin.jingjucabinet.create),
    path('admin/jingjucabinet/update',views.admin.jingjucabinet.update),
    path('admin/jingjucabinet/delete',views.admin.jingjucabinet.delete),

    path('admin/airline/list',views.admin.airline.list_api),
    path('admin/airline/create',views.admin.airline.create),
    path('admin/airline/update',views.admin.airline.update),
    path('admin/airline/delete',views.admin.airline.delete),
    path('admin/airline/import',views.admin.airline.import_excel),
    
    path('admin/baoxiu/list',views.admin.baoxiu.list_api),
    path('admin/baoxiu/create',views.admin.baoxiu.create),
    path('admin/baoxiu/update',views.admin.baoxiu.update),
    path('admin/baoxiu/delete',views.admin.baoxiu.delete),

    path('admin/returnjingju/list',views.admin.returnjingju.list_api),
    path('admin/returnjingju/create',views.admin.returnjingju.create),
    path('admin/returnjingju/update',views.admin.returnjingju.update),
    path('admin/returnjingju/delete',views.admin.returnjingju.delete),

    path('admin/diaodu/list',views.admin.diaodu.list_api),
    path('admin/diaodu/create',views.admin.diaodu.create),
    path('admin/diaodu/delete',views.admin.diaodu.delete),
]
