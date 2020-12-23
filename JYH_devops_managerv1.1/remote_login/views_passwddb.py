from django.forms import modelformset_factory
from django.test import TestCase

# Create your tests here.
from django.http import HttpResponse, request, response
from .models import RemoteManage
from .models import Passwdmanage
from .models import EstimateOpasswd
from .models import NowOpasswd
from .models import AuthUser

"""
用户登录
"""


def select_login1(username):
    try:
        server = AuthUser.objects.values_list('password').get(username='%s' % username)
        return server
    except BaseException as e:
        return None

"""
remotemanage表操作
"""


# 查询数据库开放服务器类型返回1为Linux服务器，2为windows服务器
def select_query(ip_a):
    # server = int((RemoteManage.objects.values_list('server_type').get(ip_add='%s' % ip_a))[0])
    # return server
    try:
        server = int((RemoteManage.objects.values_list('server_type').get(ip_add='%s' % ip_a))[0])
        return server
    except BaseException as e:
        return None


def select_query_name(ip_a):
    try:
        #server = (RemoteManage.objects.values_list('server_name').get(ip_add='%s' % ip_a))[0]
        server = (RemoteManage.objects.values_list('company_name').get(ip_add='%s' % ip_a))[0]
        return server
    except BaseException as e:
        return None


# 查询所有Linux服务器ip及server_name列
def select_query_linux():
    server_name = RemoteManage.objects.values_list('ip_add', 'server_name').filter(server_type='1')
    return server_name


# 查询所有windows服务器ip及server_name列
def select_query_windows():
    server_name = RemoteManage.objects.values_list('ip_add', 'server_name').filter(server_type='2')
    return server_name


"""
passwd_manage表操作
"""


# 服务器密码记录表
def est_passwd_manage(ip_a, server_name, password, gain_time):
    Passwdmanage.objects.create(ip_add=ip_a, server_name=server_name, password=password, time_stamp=gain_time)


"""
EstimateOpasswd表操作
"""


def estimate_open(ip_a, server_name, password, open_time, time_long):
    EstimateOpasswd.objects.create(ip_add=ip_a, server_name=server_name, password=password, time_stamp=open_time,
                                   time_long=time_long)


def estimate_close(ip_a):
    EstimateOpasswd.objects.filter(ip_add=ip_a).delete()


def select_estimate():
    server = EstimateOpasswd.objects.values_list('ip_add', 'time_stamp', 'time_long', "password").all()
    return server


def select_est_ip(ip_a):
    server = EstimateOpasswd.objects.values_list('time_stamp').get(ip_add='%s' % ip_a)
    return server


"""
NowOpasswd表操作
"""


def now_open(ip_a, server_type, password, time_long):
    NowOpasswd.objects.create(ip_add=ip_a, server_name=server_type, password=password, time_long=time_long)


def now_close(ip_a):
    NowOpasswd.objects.filter(ip_add=ip_a).delete()


def select_now():
    server = NowOpasswd.objects.values_list('ip_add', 'time_long', 'password').all()
    return server
