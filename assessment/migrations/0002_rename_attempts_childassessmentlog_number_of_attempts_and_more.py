# Generated by Django 4.0.6 on 2022-09-20 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("assessment", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="childassessmentlog",
            old_name="attempts",
            new_name="number_of_attempts",
        ),
        migrations.RenameField(
            model_name="childassessmentlog",
            old_name="success",
            new_name="number_of_success",
        ),
    ]
