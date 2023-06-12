# Generated by Django 4.0.6 on 2022-09-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "assessment",
            "0002_rename_attempts_childassessmentlog_number_of_attempts_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="childassessmentlog",
            old_name="number_of_success",
            new_name="number_of_correct",
        ),
        migrations.AddField(
            model_name="childassessmentlog",
            name="number_of_incorrect",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="childassessmentlog",
            name="number_of_skips",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="childassessmentlog",
            name="question_type",
            field=models.CharField(
                choices=[("EQ", "Equations"), ("WP", "Word Problems")],
                default="EQ",
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="childassessmentlog",
            name="assessment_level",
            field=models.CharField(
                choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="childassessmentlog",
            name="assessment_type",
            field=models.CharField(
                choices=[("PR", "Pre assessment"), ("PO", "Post assessment")],
                default="PO",
                max_length=2,
            ),
        ),
    ]
