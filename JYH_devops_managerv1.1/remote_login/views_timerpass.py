from threading import Thread
import threading
import os
import time
import string
import random
import re
import xlwt
import datetime
from . import views_passwddb as vp

"""
密码执行模块，开启/关闭服务器密码登录
windows采用计划任务的方式开放远程桌面登录
"""


def now_win_close(ip_a): #立即关闭windows服务器
    cmd = "/usr/bin/expect _shell_scripts/password_manage/win_close.exp %s" % ip_a
    os.system(cmd)
    print(ip_a + ": now close")


def now_linux_close(ip_a): #立即关闭linux服务器
    cmd = "/usr/bin/expect _shell_scripts/password_manage/linux_close.exp %s" % ip_a
    os.system(cmd)
    print(ip_a + ": now close")


"""
随机生产密码模块及一键关停远程服务器模块
"""


def random_passwd():
    """
    随机密码生产模块，格式为大小写及数字，不包含特殊字符
    """
    global pwd1
    compile_pwd = re.compile('^([0-9a-zA-Z]+.+)')
    src = string.ascii_letters + string.digits
    low = string.ascii_lowercase  # 生成小写
    num = string.digits  # 生成数字
    upper = string.ascii_uppercase  # 生成大写
    punct = string.punctuation  # 生成特殊
    punct1 = """%*+-.=?@[]_{}"""
    blend = random.sample(src, 6)
    low_1 = random.sample(low, 1)
    num_1 = random.sample(num, 2)
    upper_1 = random.sample(upper, 1)
    punct_1 = random.sample(punct1, 2)
    list_1 = low_1 + num_1 + upper_1 + punct_1 + blend
    random.shuffle(list_1)
    pwd = ''.join(list_1)
    if compile_pwd.match(pwd):
        pwd1 = compile_pwd.match(pwd).group()
    else:
        random_passwd()
    return pwd1


"""
开放密码期间IP加入数据库中，方便查询
"""


def timer_estimate_pwd(hours, ip_a):  # 删除预计添加数据库表中数据
    hour = float(hours)
    timer = threading.Timer(hour, vp.estimate_close, [ip_a])
    timer.start()


def timer_now_pwd(hours, ip_a, server_type, password, time_long):  # 删除数据后插入到立即开放数据库表中
    hour = float(hours)
    timer = threading.Timer(hour, vp.now_open, [ip_a, server_type, password, time_long])
    timer.start()


def timer_now_pwddel(hours, ip_a):  # 删除立即开放数据库密码表
    hour = float(hours)
    timer = threading.Timer(hour, vp.now_close, [ip_a])
    timer.start()
