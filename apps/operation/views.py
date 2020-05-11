from django.shortcuts import render
from django.views.generic.base import View
from apps.operation.forms import UserFavForm, CommentForm
from django.http import HttpResponseRedirect, JsonResponse
from apps.operation.models import UserFavorite, CourseComment, Banner
from apps.courses.models import Course
from apps.organizations.models import CourseOrg
from apps.organizations.models import Teacher


class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': "fail",
                'msg': "用户未登录",
            })

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']
            comment = CourseComment()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': "错误",
            })

class AddFavView(View):

    def post(self, request, *args, **kwargs):
        # 用户收藏，取消收藏
        # 首先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': "fail",
                'msg': "用户未登录",
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']

            #是否已收藏
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            # 如果已经收藏
            if exist_records:
                exist_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': "收藏",
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': "已收藏",
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': "课程错误",
            })

# Create your views here.
