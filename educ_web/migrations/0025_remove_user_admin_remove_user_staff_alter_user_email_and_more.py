# Generated by Django 4.2.1 on 2024-02-28 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educ_web', '0024_user_admin_user_staff_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
