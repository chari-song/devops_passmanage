# from django.forms import modelformset_factory
# from django.shortcuts import render
# from django.test import TestCase
#
# # Create your tests here.
# from django.http import HttpResponse, request, response
# from django.views.decorators.csrf import csrf_exempt
#
# from .models import RemoteManage
# from . import views_passwddb as vp
# from . import views_timerpass as vt
import re


# def test(request):
#     linux_server = []
#     data = vp.select_query_linux()
#     print(type(data), data)
#     for i in data:
#         pwd = vt.random_passwd()
#         print(i, pwd)
#         #vt.linux_pwd(i[0], pwd)
#         #linux_server.append(i[0])
#     print(linux_server)
#     return render(request, 'index.html')
#
#
# def server_type(request):
#     print("test2")
#     server = int((RemoteManage.objects.values_list('server_type').get(ip_add='192.168.6.142'))[0])
#     print(type(server))
#     print(server)
#     # a = int(server)
#     # print(type(a))
#     # print(a)
#     return HttpResponse(server)

def test(request):
    # linux_server = []
    # windows_server = []
    # linux_data = vp.select_query_linux()
    # windows_data = vp.select_query_windows()
    # for i in linux_data:
    #     print(i, i[0], i[1])
    #     linux_server.append(i[0])
    # # for i in windows_data:
    # #     windows_server.append(i[0])
    # print(linux_data, windows_data)
    #date = vp.select_query_name(ip_a='192.168.6.136')
    #tp.excel_pwd(linux_server, windows_server)
    #print(type(date), date)
    # return HttpResponse(linux_server + windows_server)
    ip_a = "192.168.6.136"
    ip_b = "192.168.6.142"
    server_name = "测试"
    password = "asdiou%!{"
    open_time = "2020-01-20 16:00:00"
    time_long = "2"
    # a = vp.select_now()
    # b = vp.select_est_ip(ip_b)[0]
    # print(type(b),b)
    # return render(request,"test.html")
    pass

from datetime import datetime
import datetime
a = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
b = datetime.datetime.now()
print(type(a), a)
print(type(b), b)
