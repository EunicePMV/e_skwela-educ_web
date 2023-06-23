# Generated by Django 4.2.1 on 2023-06-16 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0021_alter_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('submission_status', models.BooleanField(default=False)),
                ('attached_file', models.FileField(blank=True, upload_to='submission/None')),
                ('student_grade', models.FloatField(blank=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='educ_web.course')),
                ('student_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission', to='educ_web.task')),
            ],
        ),
    ]
