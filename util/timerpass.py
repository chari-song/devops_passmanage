#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 15:37
# @Author  : chari
# @File    : timerpass.py
# @Software: python3.5
import threading
import os
import time


class TimerSet:
    """
    1、定时模块，定时调用密码执行模块，开启/关闭密码，传入的时间参数单位为: 秒
    2、调用密码开关方法，打开和关闭密码登录调用密码开关方法，打开和关闭密码登录
    3、倒计时功能模块，显示密码登录开放的剩余时间
    """
    def __init__(self):
        self.p = PasswdOpenClose()

    def timer_open(self, hours, ip_addr, count):
        hour = float(hours)
        timer = threading.Timer(hour, self.p.open_passwd, [ip_addr])
        timer.start()
        timer1 = threading.Timer(hour, self.count_down, [count])
        timer1.start()

    def timer_close(self, hours, ip_addr):
        hour = float(hours)
        timer = threading.Timer(hour, self.p.close_passwd, [ip_addr])
        timer.start()

    def count_down(self, count):
        for i in range(count):
            senconds = count - i
            time.sleep(1)
            m, s = divmod(senconds, 60)
            h, m = divmod(m, 60)
            print("\r剩余时间: %02d时%02d分%02d秒" % (h, m, s), end="")


class PasswdOpenClose:
    """
    密码执行模块，开启/关闭服务器密码登录
    """

    def __init__(self):
        self.resultBean = dict()

    def close_passwd(self, ip_addr):
        cmd2 = "ansible %s -m script -a '_shell_scripts/close_password.sh'"%(ip_addr)
        os.system(cmd2)

    def open_passwd(self, ip_addr):
        cmd1 = "ansible %s -m script -a '_shell_scripts/open_password.sh'" %(ip_addr)
        os.system(cmd1)

