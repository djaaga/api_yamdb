# Generated by Django 2.2.16 on 2022-06-15 04:19

import users.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default=users.enums.UserRoles('user'), max_length=9, verbose_name='роль'),
        ),
    ]
