# Generated by Django 5.0.2 on 2024-05-08 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_repointegration_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='migrationconfig',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
