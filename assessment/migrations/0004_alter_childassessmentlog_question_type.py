# Generated by Django 4.0.6 on 2022-09-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "assessment",
            "0003_rename_number_of_success_childassessmentlog_number_of_correct_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="childassessmentlog",
            name="question_type",
            field=models.CharField(
                choices=[("EQ", "Equations"), ("WP", "Word Problems")],
                default="EQ",
                max_length=10,
            ),
        ),
    ]
