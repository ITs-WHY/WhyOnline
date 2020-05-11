from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.courses.models import Course, CourseTag, CourseResources, Video
from apps.operation.models import UserFavorite, UserCourses, CourseComment

class CourseVideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        # 获取课程章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 对view进行login的验证 通过django给的装饰器

        # 学习用户与课程的关联
        user_course = UserCourses.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 课程资料的下载
        course_resources = CourseResources.objects.filter(course=course)

        # 学习过该课程的同学还学习过的其他课程
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).exclude(course=course).order_by('-course__click_nums')[:5]
        related_courses = [user_course.course for user_course in all_courses]

        video = Video.objects.get(id=int(video_id))
        return render(request, 'course-play.html', {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):
        # 获取课程章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 对view进行login的验证 通过django给的装饰器

        # 学习用户与课程的关联
        user_course = UserCourses.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 课程资料的下载
        course_resources = CourseResources.objects.filter(course=course)

        # 学习过该课程的同学还学习过的其他课程
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).exclude(course=course).order_by('-course__click_nums')[:5]
        related_courses = [user_course.course for user_course in all_courses]

        course_comments = CourseComment.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            "course": course,
            "course_resources":course_resources,
            "related_courses": related_courses,
            "course_comments": course_comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, course_id, *args, **kwargs):
        # 获取课程章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 对view进行login的验证 通过django给的装饰器

        # 学习用户与课程的关联
        user_course = UserCourses.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 课程资料的下载
        course_resources = CourseResources.objects.filter(course=course)

        # 学习过该课程的同学还学习过的其他课程
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).exclude(course=course).order_by('-course__click_nums')[:5]
        related_courses = [user_course.course for user_course in all_courses]
        return render(request, 'course-video.html', {
            "course": course,
            "course_resources":course_resources,
            "related_courses": related_courses,
        })

class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        # 获取课程详情
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 通过课程的标签做课程的推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course_id]).order_by('-fav_nums')[:3]
        tags = course.coursetag_set.all()
        tag_list = []
        for tag in tags:
            tag_list.append(tag.tag)
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, 'course-detail.html', {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })

class CourseListView(View):
    def get(self, request, *args, **kwargs):
        # 获取课程列表信息
        all_courses = Course.objects.order_by("-add_time")
        hot_courses =  all_courses.order_by('-fav_nums')[:3]
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        search_type = 'course'
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(describe__icontains=keywords) | Q(detail__icontains=keywords))

        # 对课程进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-fav_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=5, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
            "keywords": keywords,
            "search_type": search_type,
        })

