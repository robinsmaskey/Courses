# Generated by Django 4.0.6 on 2022-10-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0008_alter_coursepreview_link_alter_coursereview_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursereview",
            name="completion_score",
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name="subunit",
            name="description",
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="subunit",
            name="link",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
