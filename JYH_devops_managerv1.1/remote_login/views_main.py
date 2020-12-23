from django.urls import reverse

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from . import views_timerpass as tp
from . import views_passwddb as pm
from datetime import datetime
import datetime
from threading import Thread
import re
import time
import os


def est_open_long(ip_add, start_time, long, pwd):  # 输入开放时长函数
    open_long = float(long) * 3600
    est_open_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')  # 获取密码开放时间日期
    est_start_day = (datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')).strftime("%Y-%m-%d")
    est_start_time = (datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')).strftime("%H:%M")
    est_end_day = (est_open_time + datetime.timedelta(hours=float(long))).strftime("%Y-%m-%d")
    est_end_time = (est_open_time + datetime.timedelta(hours=float(long))).strftime("%H:%M")
    print(est_start_day, est_start_time, "\n", est_end_day, est_end_time)
    server_type = pm.select_query(ip_add)  # 查询服务器系统 1为Linux 2为windows
    area = pm.select_query_name(ip_add)  # 获取IP地址所在的环境(测试/生产环境)
    pm.est_passwd_manage(ip_add, area, pwd, start_time)  # 更新密码保存数据库
    pm.estimate_open(ip_add, server_type, pwd, est_open_time, long)  # 插入预计开放密码表
    est_time = int((est_open_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())  # 当前时间到密码开放时间换成秒，定时任务
    est_time1 = int((est_time + open_long))  # 当前时间到密码关闭时间换成秒
    est_del = Thread(target=tp.timer_estimate_pwd, args=(est_time, ip_add), name='Thread-est')  # 删除预计开放数据库密码表
    est_del.start()
    now_create = Thread(target=tp.timer_now_pwd, args=(est_time, ip_add, server_type, pwd, long))  # 插入立即开放数据库密码表
    now_create.start()
    now_del = Thread(target=tp.timer_now_pwddel, args=(est_time1, ip_add))  # 删除立即开放数据库密码表
    now_del.start()
    if server_type == 2:
        print("预计开启windows服务器IP: %s 开放时间: %s %s 结束时间: %s %s 开放密码: %s" % (ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/estimate_win_open_close.exp %s %s %s %s %s %s" % (
            ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd)
        os.system(cmd)
    else:
        print("预计开启Linux服务器IP: %s 开放时间: %s %s 结束时间: %s %s 开放密码: %s" % (ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/estimate_linux_open_close.exp %s %s %s %s %s %s" % (
            ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd)
        os.system(cmd)


def now_open_long(ip_add, long, pwd):  # 输入开放时长函数
    open_long = float(long) * 3600
    server_type = pm.select_query(ip_add)  # 查询服务器系统 1为Linux 2为windows
    area = pm.select_query_name(ip_add)  # 获取IP地址所在的环境(测试/生产环境)
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pm.est_passwd_manage(ip_add, area, pwd, now_time)  # 更新密码保存数据库
    now_end_day = (datetime.datetime.now() + datetime.timedelta(hours=float(long))).strftime("%Y-%m-%d")
    now_end_time = (datetime.datetime.now() + datetime.timedelta(hours=float(long))).strftime("%H:%M")
    pm.now_open(ip_add, server_type, pwd, long)  # 插入立即开放密码表
    now_del = Thread(target=tp.timer_now_pwddel, args=(open_long, ip_add))  # 删除立即开放数据库密码表
    now_del.start()
    if server_type == 2:
        print("立即开启windows服务器IP: %s 结束时间: %s %s 开放密码: %s" % (ip_add, now_end_day, now_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/now_win_open_close.exp %s %s %s %s" % (
            ip_add, now_end_day, now_end_time, pwd)
        os.system(cmd)
    else:
        print("立即开启linux服务器IP: %s 结束时间: %s %s 开放密码: %s" % (ip_add, now_end_day, now_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/now_linux_open_close.exp %s %s %s %s" % (
            ip_add, now_end_day, now_end_time, pwd)
        os.system(cmd)


def est_open_timea(ip_add, start_time, end_time, pwd):  # 输入结束时间函数
    est_open_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')  # 获取密码开放时间日期
    est_start_day = (datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')).strftime("%Y-%m-%d")
    est_start_time = (datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')).strftime("%H:%M")
    est_close_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')  # 获取密码关闭时间日期
    est_end_day = (datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')).strftime("%Y-%m-%d")
    est_end_time = (datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')).strftime("%H:%M")
    long = float((est_close_time - est_open_time).total_seconds() / 3600)  # 计算开放时长
    print(est_start_day, est_start_time, "\n", est_end_day, est_end_time)
    server_type = pm.select_query(ip_add)  # 查询服务器系统 1为Linux 2为windows
    area = pm.select_query_name(ip_add)  # 获取IP地址所在的环境(测试/生产环境)
    pm.est_passwd_manage(ip_add, area, pwd, start_time)  # 更新密码保存数据库
    pm.estimate_open(ip_add, server_type, pwd, est_open_time, long)  # 插入预计开放密码表
    est_time = int(
        (est_open_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())  # 当前时间到密码开放时间换成秒
    est_time1 = int(
        (est_close_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())  # 当前时间到密码关闭时间换成秒
    est_del = Thread(target=tp.timer_estimate_pwd, args=(est_time, ip_add), name='Thread-est')  # 删除预计开放数据库密码表
    est_del.start()
    now_create = Thread(target=tp.timer_now_pwd, args=(est_time, ip_add, server_type, pwd, long))  # 插入立即开放数据库密码表
    now_create.start()
    now_del = Thread(target=tp.timer_now_pwddel, args=(est_time1, ip_add))  # 删除立即开放数据库密码表
    now_del.start()
    if server_type == 2:
        print("预计开启windows服务器IP: %s 开放时间: %s %s 结束时间: %s %s 开放密码: %s" % (ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/estimate_win_open_close.exp %s %s %s %s %s %s" % (
            ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd)
        os.system(cmd)
    else:
        # 获取Linux预计开启关闭的时间
        print("预计开启linux服务器IP: %s 开放时间: %s %s 结束时间: %s %s 开放密码: %s" % (ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/estimate_linux_open_close.exp %s %s %s %s %s %s" % (
            ip_add, est_start_day, est_start_time, est_end_day, est_end_time, pwd)
        os.system(cmd)


def now_open_time(ip_add, end_time, pwd):  # 输入结束时间函数
    est_close_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')  # 获取密码关闭时间日期
    open_long = float((est_close_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())  # 当前时间到密码关闭时间换成秒
    long = open_long / 3600
    server_type = pm.select_query(ip_add)  # 查询服务器系统 1为Linux 2为windows
    area = pm.select_query_name(ip_add)  # 获取IP地址所在的环境(测试/生产环境)
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pm.est_passwd_manage(ip_add, area, pwd, now_time)  # 更新密码保存数据库
    now_end_day = (datetime.datetime.now() + datetime.timedelta(hours=float(long))).strftime("%Y-%m-%d")
    now_end_time = (datetime.datetime.now() + datetime.timedelta(hours=float(long))).strftime("%H:%M")
    pm.now_open(ip_add, server_type, pwd, long)  # 插入立即开放密码表
    now_del = Thread(target=tp.timer_now_pwddel, args=(open_long, ip_add))  # 删除立即开放数据库密码表
    now_del.start()
    if server_type == 2:
        print("立即开启windows服务器IP: %s 结束时间: %s %s 开放密码: %s" % (ip_add, now_end_day, now_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/now_win_open_close.exp %s %s %s %s" % (
            ip_add, now_end_day, now_end_time, pwd)
        os.system(cmd)
    else:
        print("立即开启linux服务器IP: %s 结束时间: %s %s 开放密码: %s" % (ip_add, now_end_day, now_end_time, pwd))
        cmd = "/usr/bin/expect _shell_scripts/password_manage/now_linux_open_close.exp %s %s %s %s" % (
            ip_add, now_end_day, now_end_time, pwd)
        os.system(cmd)


def win_close(ip_add):
    cmd = "/usr/bin/expect _shell_scripts/password_manage/win_close.exp %s" % ip_add
    os.system(cmd)


def linux_close(ip_add):
    cmd = "/usr/bin/expect _shell_scripts/password_manage/linux_close.exp %s" % ip_add
    os.system(cmd)


def linux_modify(ip_add, pwd):
    cmd = "/usr/bin/expect _shell_scripts/password_manage/linux_modify_pwd.exp %s %s" % (ip_add, pwd)
    os.system(cmd)


def windows_modify(ip_add, pwd):
    cmd = "/usr/bin/expect _shell_scripts/password_manage/win_modify_pwd.exp %s %s" % (ip_add, pwd)
    os.system(cmd)
