# Generated by Django 4.2.1 on 2023-06-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0019_alter_task_due_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
