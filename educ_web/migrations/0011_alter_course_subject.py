# Generated by Django 4.2.1 on 2023-06-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0010_course_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
