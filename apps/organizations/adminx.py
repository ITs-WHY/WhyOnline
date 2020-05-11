import xadmin

from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
from apps.organizations.models import City

class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_position', 'age']
    search_fields = ['name', 'work_years', 'work_position', 'age']
    list_filter = ['name', 'work_years', 'work_position', 'age']
    list_editable = ['name', 'work_years', 'work_position', 'age']
    model_icon = 'fa fa-male'

class CourseOrgAdmin(object):
    list_display = ['name', 'category', 'click_nums', 'fav_nums']
    search_fields = ['name', 'category', 'click_nums', 'fav_nums']
    list_filter = ['name', 'category', 'click_nums', 'fav_nums']
    list_editable = ['name', 'category', 'click_nums', 'fav_nums']
    model_icon = 'fa fa-flag'
    style_fields = {
        "desc": "ueditor"
    }

class CityAdmin(object):
    list_display = ['id','name','desc']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']
    list_editable = ['name','desc']
    model_icon = 'fa fa-building'

xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(City,CityAdmin)