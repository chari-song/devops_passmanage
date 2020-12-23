"""JYH_devops_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views_passwddb as vp
from . import views_login_date as vm


urlpatterns = [
    path('login', vm.login, name='login'),
    path('index', vm.index, name='index'),
    path('dataform', vm.dataform, name='dataform'),
    path('pwdres', vm.pwd_res),
    path('estend', vm.pwd_estend),
    path('nowend', vm.pwd_nowend),
    path('randow', vm.random_passwds),
    path('pwdmodify', vm.pwd_modify),
    path('pwdclose', vm.pwd_close),
    # path('jyhindex', ts.index, name='test_index'),

    #path('admin/', admin.site.urls),
    #path('remote/', include(appurl)),
]
