# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EstimateOpasswd(models.Model):
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_stamp = models.CharField(max_length=35)
    time_long = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'estimate_opasswd'


class NowOpasswd(models.Model):
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_long = models.CharField(max_length=4)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'now_opasswd'


class Passwdmanage(models.Model):
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'passwdmanage'


class RemoteLoginRemotemanage(models.Model):
    ip_add = models.CharField(max_length=15)
    area = models.CharField(max_length=20, blank=True, null=True)
    server_name = models.CharField(max_length=50)
    server_type = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=10)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'remote_login_remotemanage'


class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
