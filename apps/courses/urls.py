from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentView, CourseVideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name='lesson'),
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentView.as_view(), name='comments'),
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', CourseVideoView.as_view(), name='video'),
]
