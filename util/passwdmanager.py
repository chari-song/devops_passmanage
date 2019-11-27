#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 19:26
# @Author  : chari
# @File    : passwdmanager.py
# @Software: python3.5
from mypassdb import PassManageDb
import datetime as dt
from timerpass import TimerSet
from threading import Thread

data = {"192.168.6.136": ["2019-11-27 14:59:10", 10]}#, "192.168.6.134": ["2019-11-24 20:53:00", 20]}

def main(data):
    d = data
    # 实例化数据库/实例化定时任务
    pm = PassManageDb()
    ts = TimerSet()
    thread_list = []
    for k, v in d.items():
        ip_addr = k
        predict_time = v[0]
        # 密码开放的总时长
        total_time = v[1] * 10
        # 当前时间到密码开放的时间
        start_time = int((dt.datetime.strptime(predict_time, "%Y-%m-%d %H:%M:%S") - dt.datetime.now().replace(
            microsecond=0)).total_seconds())
        # 密码开放结束的时间
        over_time = total_time + start_time
        # 数据库操作
        sql = """insert into open_close_passwd(
                ip_add, start_time, predict_time, over_time, total_time)
                values ('%s', '%s', '%s', '%s', %s)""" % (ip_addr, start_time, predict_time, over_time, v[1])
        pm.add_del_mod_db(sql)
        # 定义多线程
        t_open = Thread(target=ts.timer_open, args=(start_time, ip_addr, total_time))
        t_close = Thread(target=ts.timer_close, args=(over_time, ip_addr))
        thread_list.append(t_open)
        thread_list.append(t_close)
    for i in range(len(thread_list)):
        thread_list[i].start()

if __name__ == "__main__":
    main(data)
