# Generated by Django 2.2 on 2019-11-21 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20191120_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='Video_url'),
        ),
    ]
