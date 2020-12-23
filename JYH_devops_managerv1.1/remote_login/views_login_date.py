from django.urls import reverse

from django.shortcuts import render, redirect
from django.http import HttpResponse, request, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from . import views_timerpass as tp
from . import views_passwddb as pm
from . import views_main
from threading import Thread
from datetime import datetime
from django.contrib.auth.decorators import login_required
import datetime
import re
import threading
import string
import random
import xlwt
import os


@csrf_exempt
def login(request):
    global url
    if request.method == "GET":
        return render(request, 'login_devops.html')
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')

        login = pm.select_login1(name)[0]
        if login == password:
            request.session['status'] = True
            request.session['name'] = name
            status = 1
            url = reverse('index')
            return JsonResponse({'status': status, 'url': url})
        else:
            error_msg = "用户名或密码错误"
            return render(request, 'login_devops.html', {'error_msg': error_msg} )


def login_auth(func):
    def inner(request):
        if request.session.get('status'):#在判断网页请求的状态时，直接调用request.session从djang_session表中读取数据验证
            return func(request)
        else:
            return redirect('login')
    return inner

@csrf_exempt
@login_auth
def index(request):
    return render(request, 'index.html')

@csrf_exempt
@login_auth
def dataform(request):
    """
    判断请求方式
    获取前端数据转换为字典格式
    判断输入合法性
    调用随机密码生产方法
    调用main方法
    """
    compile_time = re.compile('^([0-1][0-9]|[2][0-3]):([0-5][0-9])$')
    compile_day = re.compile('^([2][0][1-2][0-9])-([0][1-9]|[1][0-2])-([0][1-9]|[1-2][0-9]|[3][0-1])$')
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    compile_dur = re.compile('^(\d+(\.\d+)?)$')
    data = {}
    if request.method == "GET":
        return render(request, 'openpwd.html')
    if request.method == "POST":
        ip_add = request.POST.get('IP')
        date1 = request.POST.get('date1')
        time1 = request.POST.get('time1')
        date2 = request.POST.get('date2')
        time2 = request.POST.get('time2')
        dur = request.POST.get('dur')
        ip_a = re.findall(r'\d+.\d+.\d+.\d+', ip_add)
        start_day_time = "%s %s" % (date1, time1)
        end_day_time = "%s %s" % (date2, time2)

        try:    # 判断输入格式及格式化数据
            if (not date1 or compile_day.match(date1)) and (
                    not time1 or compile_time.match(time1)):
                pass
            else:
                day_error_msg = "时间日期输入不合法或持续时长不合法"
                return render(request, 'openpwd.html', {'day_error_msg': day_error_msg})
            for i in ip_a:
                pwd = tp.random_passwd()  # 调用随机生产密码方法生产随机密码
                if compile_ip.match(i) and pm.select_query(i) is not None:
                    if dur != "":
                        if start_day_time != " ":
                            views_main.est_open_long(i, start_day_time, dur, pwd)
                        else:
                            views_main.now_open_long(i, dur, pwd)
                    else:
                        if start_day_time != " ":
                            views_main.est_open_timea(i, start_day_time, end_day_time, pwd)
                        else:
                            views_main.now_open_time(i, end_day_time, pwd)
                else:
                    ip_error_msg = "IP地址输入不合法"
                    return render(request, 'openpwd.html', {'ip_error_msg': ip_error_msg})
            return render(request,'openpwd.html')  #, {'password': pwd})
        except ValueError as e:
            return HttpResponse("输入不合法")







# def main(data, pwd):
#     d = data
#     for k, v in d.items():  # 循环判断多台服务器同时开启
#         ip_a = k
#         gain_time = v[0]  # 获取字典中的预计开放时间时间
#         # 获取Linux关闭远程登录时间
#         close_time = v[1] * 3600
#         server_type = pm.select_query(ip_a)  # 查询服务器是什么系统
#         server_name = pm.select_query_name(ip_a)
#         area = pm.select_query_name(ip_a)  # 获取IP地址所在的环境(测试/生产环境)
#         pm.passwd_manage(ip_a, area, pwd)  # 更新密码保存数据库
#         if gain_time != " ":  # 判断是否设置预计开放的时间，gain_time不为空则开启预计开启远程登录，为空则立即开启远程登录
#             open_time = datetime.datetime.strptime(gain_time, '%Y-%m-%d %H:%M:%S')
#             # 数据库操作，加入预计开放数据库，到时间后删除预计开放，加入到立即开放表中，直到开放结束删除立即开放表中数据
#             pm.estimate_open(ip_a, server_name, pwd, open_time, v[1])  # 插入预计开放密码表
#             estimateopasswd_time = int((open_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())
#             nowpasswd_time = int((estimateopasswd_time + close_time))
#             est_del = Thread(target=tp.timer_estimate_pwd, args=(estimateopasswd_time, ip_a))
#             est_del.start()  # 删除预计开放数据库密码表
#             now_create = Thread(target=tp.timer_now_pwd, args=(estimateopasswd_time, ip_a, server_name, pwd, v[1]))
#             now_create.start()  # 插入立即开放数据库密码表
#             now_del = Thread(target=tp.timer_now_pwddel, args=(nowpasswd_time, ip_a))
#             now_del.start()  # 删除立即开放数据库密码表
#             if server_type == 2:
#                 print("预计开启windows")
#                 start_day = (datetime.datetime.strptime(gain_time, '%Y-%m-%d %H:%M:%S')).strftime("%Y-%m-%d")
#                 start_time = (datetime.datetime.strptime(gain_time, '%Y-%m-%d %H:%M:%S')).strftime("%H:%M:%S")
#                 end_day = (open_time + datetime.timedelta(hours=v[1])).strftime("%Y-%m-%d")
#                 end_time = (open_time + datetime.timedelta(hours=v[1])).strftime("%H:%M:%S")
#                 t_open = Thread(target=tp.estimate_termservice, args=(ip_a, start_day, start_time, end_day, end_time, pwd))
#                 t_open.start()
#             else:
#                 # 获取Linux预计开启关闭的时间
#                 print("预计开启Linux")
#                 start_time = int((open_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())
#                 end_time = int((start_time + close_time))
#                 t_open = Thread(target=tp.timer_open, args=(start_time, ip_a, pwd))
#                 t_close = Thread(target=tp.timer_close, args=(end_time, ip_a))
#                 t_open.start()
#                 t_close.start()
#         else:
#             pm.now_open(ip_a, server_name, pwd, v[1])  # 插入立即开放密码表
#             now_del = Thread(target=tp.timer_now_pwddel, args=(close_time, ip_a))
#             now_del.start()  # 删除立即开放密码表数据
#             # 获取windows关闭远程登录时间
#             end_day = (datetime.datetime.now() + datetime.timedelta(hours=v[1])).strftime("%Y-%m-%d")
#             end_time = (datetime.datetime.now() + datetime.timedelta(hours=v[1])).strftime("%H:%M:%S")
#             print(ip_a)
#             if server_type == 2:
#                 print("立即开启windows远程登录")
#                 t_open = Thread(target=tp.now_termservice, args=(ip_a, end_day, end_time, pwd))
#                 t_open.start()
#             else:
#                 print("立即开启Linux远程登录")  # 修改密码同时开启远程登录
#                 t_open = Thread(target=tp.open_passwd, args=(ip_a, pwd))
#                 t_close = Thread(target=tp.timer_close, args=(close_time, ip_a))
#                 t_open.start()
#                 t_close.start()
#
# @csrf_exempt
# @login_auth
# def adddata(request):
#     global ip_add, area, svname, company, day_time, server_type
#     if request.method == "GET":
#         return render(request, 'adddata.html')
#     if request.method == "POST":
#         ip_add = request.POST.get('IP')
#         area = request.POST.get('area')
#         svname = request.POST.get('svname')
#         server_type = request.POST.get('server_type')
#         company = request.POST.get('company')
#         day_time = request.POST.get('day_time')
#     # print(ip_add, area, svname, server_type, company, day_time)
#     try:
#         pm.add_data(ip_add, area, svname, server_type, company, day_time)
#         return HttpResponse('添加成功 ' + ip_add)
#     except BaseException as e:
#         return HttpResponse('添加失败 ' + ip_add)

# @csrf_exempt
# @login_auth
# def modify_pwd(request):
#     linux_server = []
#     linux_server_name = []
#     windows_server = []
#     windows_server_name = []
#     # 获取数据库的所有服务器
#     linux_data = pm.select_query_linux()
#     windows_data = pm.select_query_windows()
#     for i in linux_data:
#         linux_server.append(i[0])
#         linux_server_name.append(i[1])
#     for i in windows_data:
#         windows_server.append(i[0])
#         windows_server_name.append(i[1])
#     tp.excel_pwd(linux_server, linux_server_name, windows_server, windows_server_name)
#     return HttpResponse(linux_server + linux_server_name + windows_server + windows_server_name)
#
@csrf_exempt
@login_auth
def pwd_res(request):
    """
    查询密码开放表展示到前端
    """
    now = pm.select_now()
    estimate = pm.select_estimate()
    now_ip_a = []
    now_dur = []
    now_password = []
    est_ip_a = []
    est_dur = []
    est_long = []
    est_password = []
    # if estimate:
    #     est_password = str(estimate[0][3])
    for i in estimate:
        est_ip_a.append(i[0])
        est_dur.append(i[1])
        est_long.append(i[2])
        est_password.append(i[3])
    for i in now:
        now_ip_a.append(i[0])
        now_dur.append(i[1])
        now_password.append(i[2])
    print(est_password)
    return render(request, 'openpwd.html', {'est_ip': est_ip_a, 'est_dur': est_dur, 'est_long': est_long, 'est_password': est_password,  'now_ip': now_ip_a, 'now_dur': now_dur, 'now_password': now_password })


@csrf_exempt
@login_auth
def pwd_estend(request):
    """
    获取前端预计开放的服务器IP地址进行紧急关闭密码登录
    """
    if request.method == "POST":
        ip_add = request.POST.getlist('est_ip')
        try:
            for i in ip_add:
                ip_a = i
                est_time = pm.select_est_ip(ip_a)[0]  # 查询预计开启的时间
                server_type = pm.select_query(ip_a)  # 查询服务器是什么系统
                est_end_time = datetime.datetime.strptime(est_time, '%Y-%m-%d %H:%M')
                est_endlinux_time1 = int((est_end_time - datetime.datetime.now().replace(microsecond=0)).total_seconds())
                est_endlinux_time2 = (est_endlinux_time1 + int(20))
                if server_type == 2:
                    views_main.win_close(i)
                elif server_type == 1:
                    views_main.linux_close(i)
                now_del = Thread(target=tp.timer_now_pwddel, args=(est_endlinux_time2, ip_a))
                now_del.start()  # 删除立即开放数据库密码表
                pm.estimate_close(ip_a)   # 删除预计添加表
        except BaseException as e:
            print(e)
        return pwd_res(request)

@csrf_exempt
@login_auth
def pwd_nowend(request):
    """
    获取前端立即开放密码IP地址进行紧急关闭
    """
    if request.method == "POST":
        ip_add = request.POST.getlist('now_ip')
        try:
            for i in ip_add:
                ip_a = i
                server_type = pm.select_query(ip_a)  # 查询服务器是什么系统
                if server_type == 2:
                    views_main.win_close(i)
                elif server_type == 1:
                    views_main.linux_close(i)
                pm.now_close(ip_a)  # 删除立即开放数据库密码表
        except BaseException as  e:
            print(e)
        return pwd_res(request)


@csrf_exempt
@login_auth
def random_passwds(request):
    """
    随机密码生产模块，格式为大小写及数字，不包含特殊字符展示到web页面
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
        random_passwds()
    return HttpResponse(pwd1)


@csrf_exempt
@login_auth
def pwd_close(request):
    """
    判断请求方式
    判断输入合法性
    调用main方法
    """
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if request.method == "GET":
        return render(request, 'managerpwd.html')
    if request.method == "POST":
        ip_add = request.POST.get('IP')
        ip_a = re.findall(r'\d+.\d+.\d+.\d+', ip_add)
        #print(ip_a)
        if ip_a:
            for i in ip_a:
                if compile_ip.match(i) and pm.select_query(i) is not None:
                    if pm.select_query(i) == 1:
                        views_main.linux_close(i)
                    else:
                        views_main.win_close(i)
                else:
                    ip_error_msg = "IP地址输入不合法"
                    return render(request, 'managerpwd.html', {'ip_error_msg': ip_error_msg})
        else:
            linux_ip = pm.select_query_linux()
            windows_ip = pm.select_query_windows()
            for i in linux_ip:
                #print(i[0])
                views_main.linux_close(i[0])
            for i in windows_ip:
                #print(i[0])
                views_main.win_close(i[0])
        return render(request, 'managerpwd.html', {'pwd_manage': "修改成功"})


@csrf_exempt
@login_auth
def pwd_modify(request):
    """
    判断请求方式
    判断输入合法性
    调用main方法
    """
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    count_win = 0
    count_linux = 0
    if not os.path.isdir('devops_file'):  # and os.path.isdir('log'):
        os.mkdir('devops_file')
    start_time = datetime.datetime.now().strftime("%Y_%m_%d")
    start_time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Linux修改密码')
    worksheet1 = workbook.add_sheet('Windows修改密码')
    # 行，列，值
    worksheet.write(0, 0, label=u'IP地址')
    worksheet.write(0, 1, label=u'密码')
    worksheet1.write(0, 0, label=u'IP地址')
    worksheet1.write(0, 1, label=u'密码')
    if request.method == "GET":
        return render(request, 'managerpwd.html')
    if request.method == "POST":
        ip_add = request.POST.get('IP')
        ip_a = re.findall(r'\d+.\d+.\d+.\d+', ip_add)
        if ip_a:
            for i in ip_a:
                if compile_ip.match(i) and pm.select_query(i) is not None:
                    if pm.select_query(i) == 1:
                        pwd = tp.random_passwd()  # 调用随机生产密码方法生产随机密码
                        views_main.linux_modify(i, pwd)
                        count_linux += 1
                        worksheet.write(count_linux, 0, label=u'%s' % i)  # 写入excel
                        worksheet.write(count_linux, 1, label=u'%s' % pwd)
                        pm.est_passwd_manage(i, "修改1", pwd, start_time1)  # 更新密码保存数据库
                    else:
                        pwd = tp.random_passwd()  # 调用随机生产密码方法生产随机密码
                        views_main.windows_modify(i, pwd)
                        count_win += 1
                        worksheet1.write(count_win, 0, label=u'%s' % i)  # 写入excel
                        worksheet1.write(count_win, 1, label=u'%s' % pwd)
                        pm.est_passwd_manage(i, "修改2", pwd, start_time1)  # 更新密码保存数据库
                else:
                    ip_error_msg = "IP地址输入不合法"
                    return render(request, 'managerpwd.html', {'ip_pwd_msg': ip_error_msg})
        else:
            linux_ip = pm.select_query_linux()
            windows_ip = pm.select_query_windows()
            for i in linux_ip:
                pwd = tp.random_passwd()  # 调用随机生产密码方法生产随机密码
                views_main.linux_modify(i[0], pwd)
                count_linux += 1
                worksheet.write(count_linux, 0, label=u'%s' % i[0])  # 写入excel
                worksheet.write(count_linux, 1, label=u'%s' % pwd)
                pm.est_passwd_manage(i[0], "修改1", pwd, start_time1)  # 更新密码保存数据库
            for i in windows_ip:
                pwd = tp.random_passwd()  # 调用随机生产密码方法生产随机密码
                views_main.windows_modify(i[0], pwd)
                count_win += 1
                worksheet1.write(count_win, 0, label=u'%s' % i[0])  # 写入excel
                worksheet1.write(count_win, 1, label=u'%s' % pwd)
                pm.est_passwd_manage(i[0], "修改2", pwd, start_time1)  # 更新密码保存数据库
        workbook.save('devops_file/modify_pwd_%s.xls' % start_time)
        return render(request, 'managerpwd.html', {'pwd_modify': "密码修改成功"})
