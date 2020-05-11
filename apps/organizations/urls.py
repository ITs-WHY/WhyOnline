from django.conf.urls import url
from apps.organizations.views import AddAskView, OrgViews, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeacherListView, TeacherDetailView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^list/$', OrgViews.as_view(), name='list'),
    url(r'^add_ask/$', csrf_exempt(AddAskView.as_view()), name='add_ask'),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name='teacher'),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name='course'),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name='desc'),

    # 讲师列表页
    url(r'^teachers/$', TeacherListView.as_view(), name='teachers'),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
