# Generated by Django 4.2.1 on 2023-06-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0020_alter_task_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
    ]
