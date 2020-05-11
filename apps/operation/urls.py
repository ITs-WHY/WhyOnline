from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from apps.operation.views import AddFavView, AddCommentView
urlpatterns = [
    url(r'^fav/$', AddFavView.as_view(), name='fav'),
    url(r'^comment/$', AddCommentView.as_view(), name='comment'),
]
