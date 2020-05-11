# Generated by Django 2.2 on 2019-11-13 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='address',
            field=models.CharField(default='', max_length=150, verbose_name='机构地址'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gr', '个人'), ('gx', '学校')], default='培训结构', max_length=24, verbose_name='机构类型'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.City', verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='课程数量'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.TextField(default='', verbose_name='机构描述'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='name',
            field=models.CharField(default='', max_length=10, verbose_name='机构名称'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='学生数量'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='China Known', max_length=10, verbose_name='机构标签'),
        ),
    ]