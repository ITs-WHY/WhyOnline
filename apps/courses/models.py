from apps.users.models import BaseModel

from django.db import models

from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
from DjangoUeditor.models import UEditorField

class Course(BaseModel):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='教师')
    course_org = models.ForeignKey(CourseOrg,null=True,blank=True, on_delete=models.CASCADE, verbose_name='课程机构')
    name = models.CharField(max_length=50, verbose_name='课程名字')
    describe = models.CharField(max_length=300,verbose_name='课程描述')
    learn_time = models.IntegerField(default=0,verbose_name='学习时长（分钟）')
    degree = models.CharField(choices=(('cj','简单'),('zj','中等'),('gj','需要一定基础')),max_length=9,verbose_name='难度')
    notice = models.CharField(max_length=30,verbose_name='课程公告', default='')
    students = models.IntegerField(default=0,verbose_name='学生数量')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    category = models.CharField(default='Backend',max_length=20,verbose_name='类别')
    tag = models.CharField(default='',max_length=10,verbose_name='课程标签')
    need_to_know = models.CharField(default='',max_length=300,verbose_name='学前须知')
    teacher_tell = models.CharField(default='',max_length=300,verbose_name='老师说')
    is_banner = models.BooleanField(default=False, verbose_name='是否为广告位')
    detail = UEditorField(default='',verbose_name='课程详情', width=1200, height=600, imagePath='course/ueditor/images/',
                                 filePath='course/ueditor/files')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='课程封面',max_length=100)

    is_class = models.BooleanField(default=False,verbose_name='是否经典')
    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<image src='{}'>".format(self.image.url))
    # 在列表页上显示自己想显示的内容
    show_image.short_description = "图片"
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))
    # 在列表页上显示自己想显示的内容
    go_to.short_description = "跳转链接"

class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name='课程')
    tag = models.CharField(default='', max_length=10,verbose_name='标签')

    class Meta:
        verbose_name = '课程标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag

class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=10,verbose_name='课程名称')
    learn_time = models.IntegerField(default=0, verbose_name='课程时长（分钟）')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=10, verbose_name='视频名称')
    learn_time = models.IntegerField(default=0, verbose_name='视频时长（分钟）')
    url = models.CharField(max_length=1000,verbose_name='视频url')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResources(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(default='',max_length=10,verbose_name='资源名称')
    file = models.FileField(upload_to='course/resources/%Y/%m',verbose_name='资源url',max_length=200)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True

