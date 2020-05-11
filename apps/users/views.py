from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm,RegisterPostForm,UploadImageForm
from apps.users.forms import UserInfoForm, ChangePwdForm, ChangeMobileForm
from apps.utils.submail import send_sms
from WhyOnline.settings import sm_id, sm_key, REDIS_HOST, REDIS_PORT
import random
import redis
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operation.models import UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course


class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile_phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def unread_nums(request):
    """
    Add media-related context variables to the context.
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        all_messages = UserMessage.objects.filter(user=request.user)
        # 对消息分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, per_page=1, request=request)
        messages = p.page(page)
        for message in messages.object_list:
            message.has_read = True
            message.save()
        return render(request, 'usercenter-message.html', {
            "messages":messages,
        })

class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.filter(id=fav_course.fav_id)
                course_list.append(course[0])
            except Course.DoesNotExist as e:
                pass
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.filter(id=fav_teacher.fav_id)
            teacher_list.append(teacher[0])
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })

class ChangeMobileView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, *args, **kwargs):
        mobile_form = ChangeMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data['mobile']
            # 已经存在的手机不能重复注册
            if UserProfile.objects.filter(mobile_phone=mobile):
                return JsonResponse({
                    "mobile":"该手机号已注册"
                })
            else:
                user = request.user
                user.mobile_phone = mobile
                user.username = mobile
                user.save()
                return JsonResponse({
                    "status": "success"
                })
                # login(request, user)
        else:
            return JsonResponse(mobile_form.errors)

class ChangePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            user =request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(pwd_form.errors)

class ImageUploadView(LoginRequiredMixin, View):
    login_url = '/login/'

    # def save_file(self, file):
    #     with open('/root/PycharmProjects/WhyOnline/media/head_image/2019/uploaded.jpg', 'wb') as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        # files = request.FILES['image']
        # self.save_file(files)
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status":'success',
            })
        else:
            return JsonResponse({
                "status": 'fail',
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        captcha_form = RegisterGetForm()
        current_page = 'info'
        return render(request, 'usercenter-info.html', {
            'captcha_form': captcha_form,
            "current_page": current_page,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status":'success',
            })
        else:
            return JsonResponse(user_info_form.errors)

class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        banner = Banner.objects.all()[:3]
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        captcha_form = DynamicLoginForm()
        next = request.GET.get('next', '')
        return render(request, 'login.html', {'captcha_form': captcha_form,
                                              'next':next,
                                              "banners":banner})
    def post(self, request, *args, **kwargs):
        banner = Banner.objects.all()[:3]
        dynamic_login = True
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 没有注册帐号也能登录
            mobile = login_form.cleaned_data['mobile']
            exist_users = UserProfile.objects.filter(mobile_phone=mobile)
            if exist_users:
                user = exist_users[0]
                login(request,user)
            else:
                # 新建一个用户
                user = UserProfile(username=mobile)
                password = str(random.randint(100000,999999))
                user.set_password(password)
                user.mobile_phone=mobile
                user.save()
                login(request,user)
            next = request.GET.get('next', '')
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('index'))
        else:
            captcha_form = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form,
                                                  'captcha_form':captcha_form,
                                                  'dynamic_login':dynamic_login,
                                                  "banners":banner})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data['mobile']
            code = random.randint(100000,999999)
            code = str(code)
            re_json = send_sms(sm_id, code, mobile, sm_key)
            if re_json['status'] == 'success':
                re_dict['status'] = 'success'
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 60)

            else:
                re_dict['msg'] = re_json['msg']
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self,request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        captcha_form = DynamicLoginForm()
        banner = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        return render(request, 'login.html', {'captcha_form': captcha_form,
                                              'next':next,
                                              "banners":banner})
    def post(self, request):
        login_form = LoginForm(request.POST)
        # user_name = request.POST.get('username','')
        # password = request.POST.get('password','')
        # 后端来验证登录信息
        # if not user_name:
        #     return render(request, 'login.html', {'msg': '请输入用户名'})
        # if not password:
        #     return render(request, 'login.html', {'msg': '请输入密码'})
        # if len(password) < 3:
        #     return render(request, 'login.html', {'msg': '密码格式不正确'})
        # 表单验证
        banner = Banner.objects.all()[:3]
        # 验证用户是否存在
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', '')
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {"msg": '用户名或密码错误', 'login_form': login_form, "banners":banner})
        else:
            return render(request, 'login.html', {'login_form': login_form, "banners":banner})

# Create your views here.
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        banner = Banner.objects.all()[:3]
        captcha_form = RegisterGetForm()
        return render(request, 'register.html', {'captcha_form': captcha_form, "banners":banner})

    def post(self, request, *args, **kwargs):
        banner = Banner.objects.all()[:3]
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile_phone = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            captcha_form = RegisterGetForm()
            return render(request, 'register.html', {'register_post_form': register_post_form,
                                                     'register_get_form': captcha_form,
                                                     "banners":banner})
