from django.conf.urls import url
from apps.users.views import UserInfoView, ImageUploadView, ChangePwdView, ChangeMobileView, MyFavOrgView
from apps.users.views import MyFavTeacherView, MyFavCourseView, MyMessageView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image'),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name='pwd'),
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name='mobile'),
    url(r'^mycourse/$', login_required(TemplateView.as_view(template_name='usercenter-mycourse.html'), login_url='/login/'),{"current_page":"mycourse"}, name='mycourse'),
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name='myfavorg'),
    url(r'^myfavteacher/$', MyFavTeacherView.as_view(), name='myfavteacher'),
    url(r'^myfavcourse/$', MyFavCourseView.as_view(), name='myfavcourse'),
    url(r'^messages/$', MyMessageView.as_view(), name='messages'),
]
