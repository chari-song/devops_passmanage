#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 15:17
# @Author  : chari
# @File    : mypassdb.py
# @Software: python3.5
import pymysql


class PassManageDb:
    """
    数据库操作，增删改查
    """
    def create_db(self, sql):
        db = pymysql.connect("192.168.6.134", "py_dbtest", "123", "py_db")
        cursor = db.cursor()
        sql = sql
        cursor.execute(sql)
        db.close()

    def add_del_mod_db(self, sql):
        db = pymysql.connect("192.168.6.134", "py_dbtest", "123", "py_db")
        cursor = db.cursor()
        sql = sql
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()

    def select_db(self,sql):
        db = pymysql.connect("192.168.6.134", "py_dbtest", "123", "py_db")
        cursor = db.cursor()
        sql = sql
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print("Error:unble to fetch data")
        db.close()
# 数据库建表语句
"""CREATE TABLE "open_close_passwd" (
  "id" int(11) NOT NULL AUTO_INCREMENT,
  "ip_add" varchar(15) NOT NULL,
  "start_time" varchar(40) DEFAULT NULL,
  "predict_time" varchar(20) NOT NULL,
  "over_time" varchar(40) DEFAULT NULL,
  "total_time" int(11) NOT NULL,
  "time_stamp" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY ("id")
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4
"""
