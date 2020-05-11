from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from apps.organizations.models import CourseOrg
from apps.organizations.models import City, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.organizations.forms import AddAksForm
from django.http import HttpResponseRedirect, JsonResponse
from apps.operation.models import UserFavorite


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        # 收藏状态
        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=int(teacher_id)):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'teacher_fav': teacher_fav,
            'org_fav': org_fav,
            'hot_teachers': hot_teachers,
        })

class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        search_type = 'teacher'
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords) | Q(points__icontains=keywords))
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by("-click_nums")
        # 对讲师分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=1, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'teacher_nums': teacher_nums,
            'sort':sort,
            'hot_teachers':hot_teachers,
            "search_type": search_type,
            "keywords": keywords,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'desc'

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 判断是否被收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'course'

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 判断是否被收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=5, request = request)
        courses = p.page(page)
        return render(request, 'org-detail-course.html', {
            'all_courses': courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'teacher'

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 判断是否被收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'home'
        # 从数据库中取出数据
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 判断是否被收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddAskView(View):
    # 处理用户咨询
    def post(self, request, *args, **kwargs):
        userask_form = AddAksForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({
                "status": 'success',
            })
        else:
            return JsonResponse({
                "status": 'fail',
                "msg": '错误',
            })

class OrgViews(View):
    def get(self,request, *args, **kwargs):
        #从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        # org_nums = CourseOrg.objects.count()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 搜索机构
        keywords = request.GET.get("keywords", "")
        search_type = 'org'
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(tag__icontains=keywords))
        # 通过机构类别对课程机构筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 通过cityid所在城市对城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        org_nums = all_orgs.count()
        # 对机构进行排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by("-students")
        elif sort == 'courses':
            all_orgs = all_orgs.order_by("-course_nums")
        # 对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5, request = request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
            "keywords": keywords,
            "search_type": search_type,
        })


