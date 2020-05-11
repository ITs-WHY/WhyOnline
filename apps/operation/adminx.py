import xadmin
from apps.operation.models import UserAsk, CourseComment, UserFavorite, UserCourses, UserMessage, Banner

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'course_name']
    list_filter = ['name', 'course_name', 'add_time']
    list_editable = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-handshake-o'

class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'comments', 'add_time']
    list_editable = ['user', 'course', 'comments', 'add_time']
    model_icon = 'fa fa-comment'


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    list_editable = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-thumbs-up'

class UserCoursesAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    list_editable = ['user', 'course', 'add_time']
    model_icon = 'fa fa-server'
    # 重载方法来定义修改和保存数据的逻辑
    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students += 1
            course.save()
        pass

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    list_editable = ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-send'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index']
    list_editable = ['title', 'image', 'url', 'index']
    model_icon = 'fa fa-eye'

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment,CourseCommentAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserCourses,UserCoursesAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(Banner,BannerAdmin)