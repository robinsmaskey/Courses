# Generated by Django 4.0.6 on 2022-10-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_alter_coursereview_name_alter_coursereview_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepreview',
            name='name',
            field=models.CharField(choices=[('Lesson Intro', 'Course Intro'), ('Pre Assessment', 'Pre Assessment')], max_length=255),
        ),
    ]
