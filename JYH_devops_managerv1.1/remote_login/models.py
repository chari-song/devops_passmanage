from django.db import models


# Create your models here.
class RemoteManage(models.Model):
    objects = models.Manager()
    ip_add = models.CharField(max_length=15)
    area = models.CharField(max_length=20)
    server_name = models.CharField(max_length=50, blank=True, null=True)
    server_type = models.IntegerField()
    company_name = models.CharField(max_length=10)
    time_stamp = models.DateTimeField()


class Passwdmanage(models.Model):
    objects = models.Manager()
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'passwdmanage'


class EstimateOpasswd(models.Model):
    objects = models.Manager()
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_stamp = models.CharField(max_length=35)
    time_long = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'estimate_opasswd'


class NowOpasswd(models.Model):
    objects = models.Manager()
    ip_add = models.CharField(max_length=15)
    server_name = models.CharField(max_length=50)
    password = models.CharField(max_length=12)
    time_long = models.CharField(max_length=4)
    time_stamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'now_opasswd'


class AuthUser(models.Model):
    objects = models.Manager()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'