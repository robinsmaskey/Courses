# Generated by Django 4.0.6 on 2022-10-13 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0005_lessonreview_lessonpreview_coursereview_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lessonreview",
            name="lesson",
        ),
        migrations.DeleteModel(
            name="LessonPreview",
        ),
        migrations.DeleteModel(
            name="LessonReview",
        ),
    ]
