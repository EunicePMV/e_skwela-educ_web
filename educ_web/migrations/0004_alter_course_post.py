# Generated by Django 4.2.1 on 2023-06-07 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0003_rename_course_banner_course_banner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_section', to='educ_web.post'),
        ),
    ]
