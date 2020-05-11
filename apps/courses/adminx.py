import xadmin

from apps.courses.models import Course,Lesson,Video,CourseResources,CourseTag, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

class XadminSetting(object):
    site_title = '求知网后台管理系统'
    site_footer = '求知网'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class LessonInLine(object):
    model = Lesson
    extra = 0
    # style = "tab"
    exclude = ["add_time"]

class CourseResourceInLine(object):
    model = CourseResources
    style = "tab"
    extra = 1


class CourseAdmin(object):
    list_display = ['name', 'learn_time', 'degree', 'students', 'category']
    search_fields = ['name', 'degree', 'students', 'category']
    list_filter = ['name', 'learn_time', 'degree', 'students', 'category']
    list_editable = ['name', 'learn_time', 'degree', 'students', 'category']
    # 当存在外键时

class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']
    model_icon = 'fa fa-tags'
    # 只显示当前教师的课程标签
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            list = []
            courses = self.request.user.teacher.course_set.all()
            for course in courses:
                list.append(course)
            qs = qs.filter(course__in=list)
        return qs

class LessonAdmin(object):
    list_display = ['name', 'course', 'learn_time']
    search_fields = ['name', 'course'
                     ]
    list_filter = ['name', 'course', 'learn_time']
    list_editable = ['name', 'course', 'learn_time']
    model_icon = 'fa fa-tasks'


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'learn_time', 'url']
    search_fields = ['name', 'lesson', 'url']
    list_filter = ['name', 'lesson', 'learn_time', 'url']
    list_editable = ['name', 'lesson', 'learn_time', 'url']
    model_icon = 'fa fa-video-camera'



class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'file']
    search_fields = ['name', 'course', 'file']
    list_filter = ['name', 'course', 'file']
    list_editable = ['name', 'course', 'file']
    model_icon = 'fa fa-file'
    # 只显示当前教师的课程资源
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            list = []
            courses = self.request.user.teacher.course_set.all()
            for course in courses:
                list.append(course)
            qs = qs.filter(course__in=list)
        return qs

class BannerCourseAdmin(object):
    list_display = ['name', 'learn_time', 'degree', 'students', 'category', 'teacher']
    search_fields = ['name', 'degree', 'students', 'category', 'teacher']
    list_filter = ['name', 'learn_time', 'degree', 'students', 'category', 'teacher']
    list_editable = ['name', 'learn_time', 'degree', 'students', 'category', 'teacher']
    model_icon = 'fa fa-server'
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs
from import_export import resources
class CourseResource(resources.ModelResource):

    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()

class NewCouseAdmin(object):
    import_export_args = {'import_resource_class': CourseResource, 'export_resource_class': CourseResource}
    list_display = ['name', 'learn_time', 'go_to', 'degree', 'students', 'category', 'teacher', 'show_image']
    search_fields = ['name', 'degree', 'students', 'category', 'teacher']
    list_filter = ['name', 'learn_time', 'degree', 'students', 'category', 'teacher']
    list_editable = ['name', 'learn_time', 'degree', 'students', 'category', 'teacher']
    readonly_fields = ['students', 'fav_nums', 'click_nums', 'is_banner', 'is_class']
    exclude = ['add_time']
    ordering = ['-click_nums']
    model_icon = 'fa fa-address-book'
    inlines = [LessonInLine, CourseResourceInLine]
    style_fields = {
        "detail": "ueditor"
    }
    # 只显示当前教师的课程
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs
    def get_form_layout(self):
        # 判断是否是编辑页面
        # if self.org_obj:
        self.form_layout = (
            Main(
                Fieldset('讲师信息',
                         'teacher', 'course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset('基本信息',
                         'name', 'describe',
                         Row('learn_time', 'degree'),
                         Row('category', 'tag'),
                         ),
            ),
            Side(
                Fieldset('情况',
                         'students', 'fav_nums', 'click_nums',
                         ),
            ),
            Side(
                Fieldset('选择',
                        'is_class', 'is_banner',
                        ),
            )
        )
        return super(NewCouseAdmin, self).get_form_layout()

# xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Course,NewCouseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResources,CourseResourceAdmin)
xadmin.site.register(CourseTag,CourseTagAdmin)

xadmin.site.register(xadmin.views.CommAdminView, XadminSetting)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)