from audioop import reverse

from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.test import TestCase
from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from . import views_timerpass as tp
from . import views_passwddb as pm
from threading import Thread
from datetime import datetime
from django.contrib.auth.decorators import login_required
import datetime
import re
import time
# Create your tests here.
from django.http import HttpResponse, request, response
from django.views.decorators.csrf import csrf_exempt

from .models import RemoteManage
from . import views_passwddb as vp
from . import views_timerpass as vt
from functools import wraps
import re


# def test(request):
#     if request.method == "GET":
#         return render(request, 'login_devops.html')
#     if request.method == "POST":
#         name = request.POST.get('name')
#         password = request.POST.get('password')
#         if name == "sccl" and password == "sccl@2020":
#             request.session['status'] = True
#             request.seesion['name'] = name
#             status = 1
#             url = reverse('index')
#         else:
#             status = 0
#             url = ''
#             error_msg = "用户名或密码错误"
#         return JsonResponse({'status': status, 'url': url})
#
#
# def login_auth(func):
#     def inner(request):
#         if request.seesion.get('status'):
#             return func(request)
#         else:
#             return redirect('test_login')
#     return inner
#
#
# @login_auth
# def index(request):
#     if request.method == "GET":
#         return render(request, 'index.html')
#     if request.method == "POST":
#         return render(request, 'index.html')
def test(request):
    request.session['name'] = 'sccl'
    return HttpResponse("test session")

