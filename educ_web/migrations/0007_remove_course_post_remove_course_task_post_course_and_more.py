# Generated by Django 4.2.1 on 2023-06-07 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0006_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='post',
        ),
        migrations.RemoveField(
            model_name='course',
            name='task',
        ),
        migrations.AddField(
            model_name='post',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='educ_web.course'),
        ),
        migrations.AddField(
            model_name='task',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='educ_web.course'),
        ),
    ]
