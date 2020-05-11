"""WhyOnline URL Configuration

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
from WhyOnline.settings import MEDIA_ROOT
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
# django 静态文件处理
from django.views.static import serve

import xadmin

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from apps.operation.views import IndexView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('d_login/', DynamicLoginView.as_view(), name='d_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),
    path('register/', RegisterView.as_view(), name='register'),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    #机构相关页面
    # url(r'^org_list/', OrgViews.as_view(), name='org_list'),
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),
    #用户操作相关页面
    url(r'^op/', include(('apps.operation.urls', 'operation'), namespace='op')),
    # 公开课页面
    url(r'^course/', include(('apps.courses.urls', 'courses'), namespace='course')),
    # 用户中心页面
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),

    url(r'^ueditor/',include('DjangoUeditor.urls')),
]
