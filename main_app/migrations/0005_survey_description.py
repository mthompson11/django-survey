# Generated by Django 4.0.2 on 2022-04-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_survey_users_taken_alter_survey_owner_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='description',
            field=models.CharField(default='this is a survey', max_length=255),
            preserve_default=False,
        ),
    ]