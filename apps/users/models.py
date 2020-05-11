from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
gender_choice = (
    ('male', 'man'),
    ('female', 'woman')
)


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称',default='')
    birthday = models.DateField(verbose_name='生日',null=True,blank=True)
    gender = models.CharField(verbose_name='性别',choices=gender_choice, max_length=6)
    address = models.CharField(max_length=100,verbose_name='地址', default='')
    mobile_phone = models.CharField(max_length=11,verbose_name='电话号码')#the number is unique
    image = models.ImageField(upload_to='head_image/%Y',default='default.jpg',verbose_name='头像')
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        return self.username
# Create your models here.
