# Generated by Django 4.0.3 on 2022-04-18 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_alter_survey_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='user',
            new_name='owner',
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250)),
                ('option_one', models.CharField(max_length=200)),
                ('option_two', models.CharField(max_length=200)),
                ('option_three', models.CharField(max_length=200)),
                ('option_one_votes', models.IntegerField(default=0)),
                ('option_two_votes', models.IntegerField(default=0)),
                ('option_three_votes', models.IntegerField(default=0)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.survey')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_taken', models.ManyToManyField(to='main_app.survey')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
