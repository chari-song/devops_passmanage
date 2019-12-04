#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 19:05
# @Author  : chari
# @File    : smtp.py
# @Software: python3.5
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json


class Emails:
    """
    SMTP服务邮件测试
    """
    def __init__(self):
        self.mail_host = 'smtp.qq.com'
        self.mail_user = '1044067992@qq.com'
        self.mail_pass = 'jnlhhkxjmvaybbbc'

    def sende(self, subject, receive_email, data):
        message = MIMEText(data, "plain", "utf-8")
        message['From'] = Header("赤河子", "utf-8")
        message['To'] = Header("测试", "utf-8")
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpobj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpobj.login(self.mail_user, self.mail_pass)
            smtpobj.sendmail(self.mail_user, receive_email, message.as_string())
            smtpobj.quit()
            print("发送成功")
        except smtplib.SMTPException:
            print("ERROR: 发送失败")


def main():
    emails = Emails()
    receive_email = 'xiaosongcgari@163.com'
    d = {
        "%Cpu(s)": "60.0 us",
        "available": "731M",
        "/": "24%"
    }
    data = json.dumps(d, indent=4)
    print(data)
    emails.sende('这是主题', receive_email, data)


if __name__ == "__main__":
    main()

