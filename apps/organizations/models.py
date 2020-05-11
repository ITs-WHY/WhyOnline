from django.db import models

from apps.users.models import BaseModel
from DjangoUeditor.models import UEditorField
class City(BaseModel):
    name = models.CharField(max_length=20,verbose_name="城市名称")
    desc = models.CharField(max_length=200,verbose_name='描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(BaseModel):
    name = models.CharField(default='',max_length=10, verbose_name='机构名称')
    desc = UEditorField(default='',verbose_name='机构描述', width=1200, height=600, imagePath='org/ueditor/images/',
                                 filePath='org/ueditor/files')
    tag = models.CharField(default='China Known',max_length=11,verbose_name='机构标签')
    category = models.CharField(default='培训结构', verbose_name='机构类型',
                                max_length=24, choices=(('pxjg','培训机构'),
                                                        ('gr','个人'), ('gx','学校')))
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(default='', max_length=150, verbose_name='机构地址')
    students = models.IntegerField(default=0, verbose_name='学生数量')
    course_nums = models.IntegerField(default=0, verbose_name='课程数量')
    city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name='城市')

    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    def courses(self):
        # from apps.courses.models import Course
        # courses = Course.objects.filter(course_org=self)
        courses = self.course_set.filter(is_class=True)[:3]
        return courses

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

from apps.users.models import UserProfile
class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name='所属机构')
    name = models.CharField(default='', max_length=10,verbose_name="教师姓名")
    work_years = models.IntegerField(default=0, verbose_name='工作经验')
    work_company = models.CharField(default='',max_length=50,verbose_name='工作公司')
    work_position = models.CharField(default='',max_length=10,verbose_name="工作职位")
    points = models.CharField(max_length=50,verbose_name='特点')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    age = models.IntegerField(default=0,verbose_name='教师年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m',verbose_name='头像',max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return str(self.course_set.all().count())